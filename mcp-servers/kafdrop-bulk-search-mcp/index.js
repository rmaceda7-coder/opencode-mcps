import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const KAFDROP_URLS = {
  dev:     (process.env.KAFDROP_BASE_URL_DEV     ?? "https://sharedeks01-na1.infra.dev.internal/kafdrop").replace(/\/$/, ""),
  test:    (process.env.KAFDROP_BASE_URL_TEST    ?? "https://sharedeks01-na1.infra.test.internal/kafdrop").replace(/\/$/, ""),
  staging: (process.env.KAFDROP_BASE_URL_STAGING ?? "https://sharedeks01-na1.infra.staging.internal/kafdrop").replace(/\/$/, ""),
  perf:    (process.env.KAFDROP_BASE_URL_PERF    ?? "https://sharedeks01-na1.infra.perf.internal/kafdrop").replace(/\/$/, ""),
};

const ENV_ALIASES = {
  dev: "dev", development: "dev",
  test: "test", testing: "test",
  staging: "staging", stage: "staging",
  perf: "perf", performance: "perf",
};

function resolveUrl(environment) {
  const key = ENV_ALIASES[environment?.toLowerCase()];
  if (!key) throw new Error(`Unknown environment '${environment}'. Valid values: dev, test, staging, perf.`);
  return KAFDROP_URLS[key];
}

// Validate that at least one URL is configured
const hasAnyUrl = Object.values(KAFDROP_URLS).some(Boolean);
if (!hasAnyUrl) {
  console.error("ERROR: No KAFDROP_BASE_URL_* environment variables are set.");
  process.exit(1);
}

const BATCH_SIZE = 100; // Kafdrop max per request

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Fetch messages from Kafdrop REST API with Protobuf decoding.
 */
async function fetchMessages(baseUrl, topic, partition, offset, count = BATCH_SIZE) {
  const url = new URL(
    `${baseUrl}/topic/${encodeURIComponent(topic)}/messages`
  );
  url.searchParams.set("partition", partition);
  url.searchParams.set("offset", offset);
  url.searchParams.set("count", count);
  url.searchParams.set("keyFormat", "DEFAULT");
  url.searchParams.set("format", "PROTOBUF");
  url.searchParams.set("isAnyProto", "false");

  const res = await fetch(url.toString(), {
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Kafdrop responded ${res.status} for partition ${partition} offset ${offset}`);
  }

  return res.json();
}

/**
 * Fetch topic metadata (partition offsets) from Kafdrop.
 */
async function fetchTopicDetails(baseUrl, topic) {
  const url = `${baseUrl}/topic/${encodeURIComponent(topic)}`;
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`Kafdrop responded ${res.status} fetching topic details`);
  return res.json();
}

/**
 * Parse a Protobuf text-format message into a key/value object.
 * Handles scalar fields: field_name: "value" or field_name: 123
 * Nested blocks (timestamps) are flattened as field_name.sub_field.
 */
function parseProtoText(text, prefix = "") {
  const result = {};
  const lines = text.split("\n");
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();

    if (!line || line === "{" || line === "}") {
      i++;
      continue;
    }

    // Nested block: field_name {
    const blockMatch = line.match(/^(\w+)\s*\{$/);
    if (blockMatch) {
      const blockLines = [];
      i++;
      let depth = 1;
      while (i < lines.length && depth > 0) {
        const inner = lines[i].trim();
        if (inner.endsWith("{")) depth++;
        if (inner === "}") depth--;
        if (depth > 0) blockLines.push(lines[i]);
        i++;
      }
      const nested = parseProtoText(blockLines.join("\n"), `${prefix}${blockMatch[1]}.`);
      Object.assign(result, nested);
      continue;
    }

    // Scalar field: key: value
    const fieldMatch = line.match(/^(\w+):\s*(.+)$/);
    if (fieldMatch) {
      const key = `${prefix}${fieldMatch[1]}`;
      const raw = fieldMatch[2].trim();
      // Strip surrounding quotes if present
      result[key] = raw.startsWith('"') && raw.endsWith('"')
        ? raw.slice(1, -1)
        : raw;
    }

    i++;
  }

  return result;
}

/**
 * Estimate the starting offset for a given lookback period in hours
 * by binary-searching based on message timestamps.
 * Falls back to firstOffset if estimation fails.
 */
async function estimateOffsetForTime(baseUrl, topic, partition, targetMs) {
  const details = await fetchTopicDetails(baseUrl, topic);
  const partitionInfo = details.partitions?.find((p) => p.partition === partition);
  if (!partitionInfo) throw new Error(`Partition ${partition} not found in topic ${topic}`);

  let lo = partitionInfo.firstOffset ?? 0;
  let hi = partitionInfo.size - 1;

  // Quick boundary check — fetch last message timestamp
  const lastBatch = await fetchMessages(baseUrl, topic, partition, hi, 1);
  if (!lastBatch?.length) return lo;

  const lastTs = new Date(lastBatch[0].timestamp).getTime();
  if (targetMs >= lastTs) return hi; // target is after last message, return end

  // Binary search for approximate offset
  let iterations = 0;
  while (lo < hi - 1 && iterations < 30) {
    const mid = Math.floor((lo + hi) / 2);
    const batch = await fetchMessages(baseUrl, topic, partition, mid, 1);
    if (!batch?.length) break;

    const ts = new Date(batch[0].timestamp).getTime();
    if (ts < targetMs) {
      lo = mid;
    } else {
      hi = mid;
    }
    iterations++;
  }

  return lo;
}

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: "kafdrop-bulk-search",
  version: "1.0.0",
});

const environmentParam = z
  .string()
  .optional()
  .default("staging")
  .describe("Target environment: 'dev', 'test', 'staging', or 'perf' (default: 'staging')");

// ---------------------------------------------------------------------------
// Tool 1: get_partition_offsets
// ---------------------------------------------------------------------------
server.tool(
  "get_partition_offsets",
  "Get partition metadata and estimate the starting offset for a given lookback window (e.g. last 2 days).",
  {
    topic: z.string().describe("Kafka topic name"),
    lookback_hours: z
      .number()
      .optional()
      .default(48)
      .describe("How many hours back to estimate the start offset (default: 48)"),
    environment: environmentParam,
  },
  async ({ topic, lookback_hours, environment }) => {
    const baseUrl = resolveUrl(environment);
    const details = await fetchTopicDetails(baseUrl, topic);
    const targetMs = Date.now() - lookback_hours * 60 * 60 * 1000;

    const partitionSummaries = await Promise.all(
      (details.partitions ?? []).map(async (p) => {
        let estimatedOffset = null;
        try {
          estimatedOffset = await estimateOffsetForTime(baseUrl, topic, p.partition, targetMs);
        } catch {
          estimatedOffset = p.firstOffset;
        }
        return {
          partition: p.partition,
          firstOffset: p.firstOffset,
          lastOffset: p.size - 1,
          estimatedOffsetForLookback: estimatedOffset,
          approxMessagesInWindow: (p.size - 1) - estimatedOffset,
        };
      })
    );

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              topic,
              environment,
              lookback_hours,
              targetTime: new Date(targetMs).toISOString(),
              partitions: partitionSummaries,
            },
            null,
            2
          ),
        },
      ],
    };
  }
);

// ---------------------------------------------------------------------------
// Tool 2: bulk_search_by_field
// ---------------------------------------------------------------------------
server.tool(
  "bulk_search_by_field",
  "Scan a large range of Protobuf-decoded Kafka messages and filter by a specific field value. Iterates in batches of 100.",
  {
    topic: z.string().describe("Kafka topic name"),
    partition: z.number().describe("Partition number to scan"),
    start_offset: z.number().describe("Offset to start scanning from"),
    end_offset: z
      .number()
      .optional()
      .describe("Offset to stop scanning at (defaults to latest)"),
    field: z.string().describe("Field name to filter by (e.g. tenant_id)"),
    value: z.string().describe("Expected field value to match"),
    max_results: z
      .number()
      .optional()
      .default(50)
      .describe("Stop after finding this many matches (default: 50)"),
    max_batches: z
      .number()
      .optional()
      .default(200)
      .describe("Max number of 100-message batches to scan (default: 200 = 20,000 messages)"),
    environment: environmentParam,
  },
  async ({ topic, partition, start_offset, end_offset, field, value, max_results, max_batches, environment }) => {
    const baseUrl = resolveUrl(environment);
    const details = await fetchTopicDetails(baseUrl, topic);
    const partitionInfo = details.partitions?.find((p) => p.partition === partition);
    const lastOffset = end_offset ?? (partitionInfo?.size - 1) ?? start_offset + 10000;

    const matches = [];
    let scanned = 0;
    let currentOffset = start_offset;
    let batches = 0;

    while (
      currentOffset <= lastOffset &&
      matches.length < max_results &&
      batches < max_batches
    ) {
      const count = Math.min(BATCH_SIZE, lastOffset - currentOffset + 1);
      let batch;

      try {
        batch = await fetchMessages(baseUrl, topic, partition, currentOffset, count);
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ error: err.message, scanned, matches }, null, 2),
            },
          ],
        };
      }

      if (!batch?.length) break;

      for (const msg of batch) {
        scanned++;
        const parsed = parseProtoText(msg.message ?? "");
        if (parsed[field] === value) {
          matches.push({
            partition: msg.partition,
            offset: msg.offset,
            timestamp: msg.timestamp,
            key: msg.key,
            fields: parsed,
          });
          if (matches.length >= max_results) break;
        }
      }

      currentOffset = (batch[batch.length - 1]?.offset ?? currentOffset) + 1;
      batches++;
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              topic,
              partition,
              environment,
              field,
              value,
              scanned,
              batches,
              matchesFound: matches.length,
              reachedEnd: currentOffset > lastOffset,
              stoppedEarly: matches.length >= max_results,
              matches,
            },
            null,
            2
          ),
        },
      ],
    };
  }
);

// ---------------------------------------------------------------------------
// Tool 3: get_message_at_offset
// ---------------------------------------------------------------------------
server.tool(
  "get_message_at_offset",
  "Fetch and decode a single Protobuf message by topic, partition and offset.",
  {
    topic: z.string().describe("Kafka topic name"),
    partition: z.number().describe("Partition number"),
    offset: z.number().describe("Message offset"),
    environment: environmentParam,
  },
  async ({ topic, partition, offset, environment }) => {
    const baseUrl = resolveUrl(environment);
    const batch = await fetchMessages(baseUrl, topic, partition, offset, 1);
    if (!batch?.length) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: "No message found at this offset" }) }],
      };
    }

    const msg = batch[0];
    const parsed = parseProtoText(msg.message ?? "");

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              partition: msg.partition,
              offset: msg.offset,
              timestamp: msg.timestamp,
              key: msg.key,
              environment,
              fields: parsed,
            },
            null,
            2
          ),
        },
      ],
    };
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
const transport = new StdioServerTransport();
await server.connect(transport);
console.error(`kafdrop-bulk-search MCP running — environments: dev=${KAFDROP_URLS.dev}, test=${KAFDROP_URLS.test}, staging=${KAFDROP_URLS.staging}, perf=${KAFDROP_URLS.perf}`);
