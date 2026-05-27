#!/usr/bin/env python3
"""
Kafdrop MCP Server
Wraps the Kafdrop REST API to expose Kafka topic/message browsing as MCP tools.

Environment variables:
  KAFDROP_URL_DEV      - Kafdrop URL for dev     (default: https://sharedeks01-na1.infra.dev.internal/kafdrop/)
  KAFDROP_URL_TEST     - Kafdrop URL for test     (default: https://sharedeks01-na1.infra.test.internal/kafdrop/)
  KAFDROP_URL_STAGING  - Kafdrop URL for staging  (default: https://sharedeks01-na1.infra.staging.internal/kafdrop/)
  KAFDROP_URL_PERF     - Kafdrop URL for performance (default: https://sharedeks01-na1.infra.perf.internal/kafdrop/)
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

KAFDROP_URLS = {
    "dev":     os.environ.get("KAFDROP_URL_DEV",     "https://sharedeks01-na1.infra.dev.internal/kafdrop/").rstrip("/"),
    "test":    os.environ.get("KAFDROP_URL_TEST",    "https://sharedeks01-na1.infra.test.internal/kafdrop/").rstrip("/"),
    "staging": os.environ.get("KAFDROP_URL_STAGING", "https://sharedeks01-na1.infra.staging.internal/kafdrop/").rstrip("/"),
    "perf":    os.environ.get("KAFDROP_URL_PERF",    "https://sharedeks01-na1.infra.perf.internal/kafdrop/").rstrip("/"),
}

ENV_ALIASES = {
    "dev": "dev", "development": "dev",
    "test": "test", "testing": "test",
    "staging": "staging", "stage": "staging",
    "perf": "perf", "performance": "perf",
}

mcp = FastMCP("kafdrop")


def _resolve_url(environment: str) -> str:
    key = ENV_ALIASES.get(environment.lower())
    if key is None:
        raise ValueError(f"Unknown environment '{environment}'. Valid values: dev, test, staging, perf.")
    return KAFDROP_URLS[key]


def _client(environment: str) -> httpx.Client:
    return httpx.Client(base_url=_resolve_url(environment), timeout=30, verify=False)


# ---------------------------------------------------------------------------
# Tool: list_topics
# ---------------------------------------------------------------------------
@mcp.tool()
def list_topics(environment: str = "staging") -> list[dict]:
    """
    List all Kafka topics available in Kafdrop.

    Args:
        environment: Target environment — 'dev', 'test', 'staging', or 'perf' (default: 'staging').
    """
    with _client(environment) as c:
        resp = c.get("/topic", headers={"Accept": "application/json"})
        resp.raise_for_status()
        topics = resp.json()
    return [
        {
            "name": t.get("name"),
            "partitions": t.get("partitionCount", 0),
            "replicationFactor": t.get("replicationFactor", 0),
        }
        for t in topics
    ]


# ---------------------------------------------------------------------------
# Tool: get_topic_details
# ---------------------------------------------------------------------------
@mcp.tool()
def get_topic_details(topic: str, environment: str = "staging") -> dict:
    """
    Get detailed information about a Kafka topic including partitions,
    offsets, and consumer groups.

    Args:
        topic: The Kafka topic name.
        environment: Target environment — 'dev', 'test', 'staging', or 'perf' (default: 'staging').
    """
    with _client(environment) as c:
        resp = c.get(f"/topic/{topic}", headers={"Accept": "application/json"})
        resp.raise_for_status()
        data = resp.json()

    partitions = [
        {
            "partition": p.get("id"),
            "leader": p.get("leader"),
            "firstOffset": p.get("firstOffset"),
            "lastOffset": p.get("lastOffset"),
            "size": p.get("size", 0),
            "replicas": p.get("replicas", []),
        }
        for p in data.get("partitions", [])
    ]

    return {
        "name": data.get("name"),
        "partitionCount": data.get("partitionCount"),
        "replicationFactor": data.get("replicationFactor"),
        "partitions": partitions,
    }


# ---------------------------------------------------------------------------
# Tool: read_messages
# ---------------------------------------------------------------------------
@mcp.tool()
def read_messages(
    topic: str,
    partition: int = 0,
    offset: int = 0,
    count: int = 10,
    key_format: str = "DEFAULT",
    message_format: str = "DEFAULT",
    key_deserializer: str = "",
    message_deserializer: str = "",
    environment: str = "staging",
) -> list[dict]:
    """
    Read messages from a Kafka topic partition via Kafdrop.

    Args:
        topic:                The Kafka topic name.
        partition:            Partition number to read from (default: 0).
        offset:               Starting offset (default: 0). Use -1 for the last N messages.
        count:                Number of messages to return (default: 10, max: 100).
        key_format:           Key deserialization format: DEFAULT, STRING, AVRO, PROTOBUF (default: DEFAULT).
        message_format:       Message deserialization format: DEFAULT, STRING, AVRO, PROTOBUF (default: DEFAULT).
        key_deserializer:     Optional schema registry class for key (only if format is AVRO/PROTOBUF).
        message_deserializer: Optional schema registry class for message (only if format is AVRO/PROTOBUF).
        environment:          Target environment — 'dev', 'test', 'staging', or 'perf' (default: 'staging').
    """
    count = min(count, 100)  # guard against very large requests

    # If offset is -1 (tail), resolve the actual last offset for this partition
    # and compute start = lastOffset - count, mirroring the C# KafkaReader behaviour.
    if offset == -1:
        details = get_topic_details(topic, environment)
        part_info = next(
            (p for p in details["partitions"] if p["partition"] == partition), None
        )
        if part_info:
            last = part_info.get("lastOffset") or part_info.get("size", count)
            offset = max(last - count, part_info.get("firstOffset", 0))
        else:
            offset = 0

    # Kafdrop on this cluster expects partition as a query-string parameter,
    # NOT as a path segment (e.g. /topic/{name}/messages?partition=0&offset=...&isAnyProto=false).
    # Using the path-segment form (/topic/{name}/{partition}/messages) returns 404
    # for topics whose names contain dots.
    params: dict = {
        "partition": partition,
        "offset": offset,
        "count": count,
        "keyFormat": key_format,
        "format": message_format,
        "isAnyProto": "false",
    }
    if key_deserializer:
        params["keyDeserializer"] = key_deserializer
    if message_deserializer:
        params["msgDeserializer"] = message_deserializer

    with _client(environment) as c:
        url = f"/topic/{topic}/messages"
        resp = c.get(url, params=params, headers={"Accept": "application/json"})
        resp.raise_for_status()
        data = resp.json()

    messages = data if isinstance(data, list) else data.get("messages", [])
    return [
        {
            "partition": m.get("partition"),
            "offset": m.get("offset"),
            "key": m.get("key"),
            "message": m.get("message"),
            "timestamp": m.get("timestamp"),
            "headers": m.get("headers", {}),
        }
        for m in messages
    ]


# ---------------------------------------------------------------------------
# Tool: search_messages
# ---------------------------------------------------------------------------
@mcp.tool()
def search_messages(
    topic: str,
    search_text: str,
    partition: int = -1,
    offset: int = -1,
    count: int = 50,
    message_format: str = "DEFAULT",
    environment: str = "staging",
) -> list[dict]:
    """
    Search for messages containing a specific text across one or all partitions of a topic.
    Reads 'count' messages starting at 'offset' and filters client-side by 'search_text'.

    Args:
        topic:          The Kafka topic name.
        search_text:    Text to search for in message content (case-insensitive).
        partition:      Partition to search in (-1 = all partitions, default: -1).
        offset:         Starting offset per partition (default: -1 = tail, i.e. last N messages).
        count:          Max messages to scan per partition (default: 50, max: 100).
        message_format: Message deserialization format: DEFAULT, STRING, AVRO, PROTOBUF (default: DEFAULT).
        environment:    Target environment — 'dev', 'test', 'staging', or 'perf' (default: 'staging').
    """
    count = min(count, 100)

    # Determine which partitions to scan
    details = get_topic_details(topic, environment)
    if partition >= 0:
        partitions_to_scan = [p for p in details["partitions"] if p["partition"] == partition]
    else:
        partitions_to_scan = details["partitions"]

    results = []
    search_lower = search_text.lower()

    for part_info in partitions_to_scan:
        part = part_info["partition"]
        # Resolve tail offset per partition when offset == -1
        if offset == -1:
            last = part_info.get("lastOffset") or part_info.get("size", count)
            part_offset = max(last - count, part_info.get("firstOffset", 0))
        else:
            part_offset = offset

        messages = read_messages(
            topic=topic,
            partition=part,
            offset=part_offset,
            count=count,
            message_format=message_format,
            environment=environment,
        )
        for m in messages:
            msg_str = str(m.get("message", "")).lower()
            key_str = str(m.get("key", "")).lower()
            if search_lower in msg_str or search_lower in key_str:
                results.append(m)

    return results


if __name__ == "__main__":
    mcp.run(transport="stdio")
