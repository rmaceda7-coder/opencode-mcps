# OpenCode MCP Servers Configuration

This repository contains the complete OpenCode MCP (Model Context Protocol) server configuration and custom implementations used in my development environment.

## Overview

This setup includes **11 MCP servers** that extend OpenCode with various capabilities:

### Remote MCP Servers
- **Atlassian** - Jira/Confluence integration
- **GitHub** - GitHub API integration

### Local MCP Servers
- **Serena** - Code intelligence and analysis
- **Test Plan Creator** - Automated test plan generation from JIRA/Confluence
- **Snowflake** - Snowflake database access and queries
- **Kafdrop** - Kafka message browser (4 environments: dev/test/staging/perf)
- **Kafdrop Bulk Search** - Advanced Kafka message search
- **Kinesis Reader** - AWS Kinesis stream reader (dev/test/staging environments)
- **SQL Server** - SQL Server management and queries

## Repository Structure

```
opencode-mcps/
├── opencode.json              # Main OpenCode configuration file
├── docs/                      # Complete documentation suite
│   ├── 01_OpenCode_Installation_Guide.md
│   ├── 02_Serena_Code_Intelligence_Guide.md
│   ├── 03_Understanding_Serena_vs_MCP.md
│   ├── 04_GitHub_MCP_Installation_Guide.md
│   ├── 05_Atlassian_MCP_Installation_Guide.md
│   ├── 06_Azure_DevOps_TFS_MCP_Guide.md
│   ├── SQL_Server_MCP_Installation_Complete.md
│   └── (PDF versions and summaries)
└── mcp-servers/               # Custom MCP server implementations
    ├── kafdrop/
    ├── kafdrop-bulk-search-mcp/
    └── sql-server-mcp/
```

## Installation

### Prerequisites
- OpenCode installed
- Python 3.x (for Python-based servers)
- Node.js (for JavaScript-based servers)
- Java 11+ (for Test Plan Creator)
- .NET (for Kinesis Reader)

### Setup Steps

1. **Clone this repository:**
   ```bash
   git clone https://github.com/rmaceda7-coder/opencode-mcps.git
   cd opencode-mcps
   ```

2. **Copy the configuration file:**
   - Windows: Copy `opencode.json` to `%USERPROFILE%\.config\opencode\`
   - macOS/Linux: Copy `opencode.json` to `~/.config/opencode/`

3. **Update paths in opencode.json:**
   - Replace `C:\Users\ramiro.maceda\` with your actual user directory
   - Update paths to MCP server executables/scripts

4. **Set up environment variables:**
   - Snowflake: `SF_USERNAME`, `SF_PASSWORD`
   - GitHub: Update the bearer token in the configuration
   - Kafdrop/Kinesis: Configure environment-specific URLs and credentials

5. **Install custom MCP servers:**
   - Follow the installation guides in the `docs/` folder for each server

## Configuration Details

### Serena (Code Intelligence)
Uses `uvx` to run from the GitHub repository. Provides IDE-level code intelligence and analysis.

### Atlassian MCP
Remote server for Jira and Confluence integration. Requires authentication setup.

### Test Plan Creator
Java-based tool for generating test plans from JIRA epics and Confluence pages.

### Snowflake
Requires credentials file and service configuration at `%USERPROFILE%\.mcp\tools_config.yaml`.

### Kafdrop Servers
- **kafdrop**: Basic message browsing across 4 environments
- **kafdrop-bulk-search**: Advanced search with Protobuf decoding

### Kinesis Reader
Three separate instances configured for different AWS environments (dev/test/staging).
Requires AWS credential files in `C:\Temp\`.

### SQL Server
Python-based MCP server for SQL Server management, queries, and monitoring.

## Documentation

Comprehensive documentation is available in the `docs/` folder:

- **Installation Guides** - Step-by-step setup for each MCP server
- **User Guides** - How to use Serena and other features
- **Comparison Docs** - Understanding different MCP capabilities
- **Quick Reference** - Fast lookup for common tasks

All guides are available in both Markdown and PDF formats.

## External Dependencies

Some MCP servers reference external projects not included in this repository:

- **Kinesis Reader**: `C:\Users\ramiro.maceda\data-acd-automation-core\kinesis-reader-mcp`
- **Test Plan Creator**: `C:\Users\ramiro.maceda\AITestPlanGenerator\utility-suite-data-qa-automation-ai-framework`

These are proprietary tools and must be built/installed separately.

## Security Notes

- The included `opencode.json` contains placeholder/example credentials
- Update all tokens, passwords, and API keys before use
- Never commit actual credentials to version control
- Use environment variables for sensitive data

## Troubleshooting

1. **MCP Server not starting**: Check paths in opencode.json match your system
2. **Authentication errors**: Verify environment variables and credential files
3. **Command not found**: Ensure Python/Node/Java are in your PATH
4. **Connection issues**: Verify network access to internal URLs (VPN may be required)

For detailed troubleshooting, refer to the specific guide in the `docs/` folder.

## Contributing

This is a personal configuration repository. Feel free to fork and adapt for your own use.

## License

Documentation and configuration files are provided as-is for reference purposes.
