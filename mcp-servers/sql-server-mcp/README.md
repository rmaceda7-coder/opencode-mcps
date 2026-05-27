# SQL Server Management MCP Server

A Model Context Protocol (MCP) server for comprehensive SQL Server management using Windows Authentication.

## Features

- **Table Management**: Query, list, and inspect dbo schema tables
- **Data Modification**: Update, insert, and delete operations (DEV environments only: DOA, DOB)
- **SQL Agent Jobs**: Monitor job status and execution history
- **Instance Management**: Check server status and restart services
- **Windows Authentication**: Seamless integration with existing UCN credentials

## Requirements

- Python 3.9 or higher
- Windows OS
- SQL Server with Windows Authentication enabled
- Administrator privileges (for service restart operations)
- ODBC Driver 17 for SQL Server

## Installation

### 1. Install ODBC Driver

Download and install [Microsoft ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### 2. Install Python Dependencies

```bash
cd sql-server-mcp
pip install -e .
```

### 3. Configure OpenCode

Add to your OpenCode configuration file (`~/.config/opencode/config.json` or workspace `.opencode/config.json`):

```json
{
  "mcpServers": {
    "sql-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:/path/to/sql-server-mcp",
      "env": {}
    }
  }
}
```

## Available Tools

### Table Operations

#### list_tables
List all tables in the dbo schema.
```
Parameters:
  - server_name: SQL Server instance (e.g., 'DOA-SERVER\INSTANCE')
  - database_name: Target database
```

#### get_table_schema
Get detailed schema information for a table.
```
Parameters:
  - server_name: SQL Server instance
  - database_name: Target database
  - table_name: Table name
```

#### query_table
Execute SELECT queries on dbo tables.
```
Parameters:
  - server_name: SQL Server instance
  - database_name: Target database
  - table_name: Table name
  - columns: Comma-separated columns (optional, default: *)
  - where_clause: WHERE condition (optional)
  - top_n: Max rows (optional, default: 100)
```

#### update_table (DEV ONLY: DOA, DOB)
Update records in a table.
```
Parameters:
  - server_name: Must be DOA or DOB environment
  - database_name: Target database
  - table_name: Table name
  - set_clause: SET clause (e.g., "status = 'active'")
  - where_clause: WHERE condition (REQUIRED)
```

#### insert_into_table (DEV ONLY: DOA, DOB)
Insert records into a table.
```
Parameters:
  - server_name: Must be DOA or DOB environment
  - database_name: Target database
  - table_name: Table name
  - columns: Comma-separated column names
  - values: Comma-separated values
```

#### delete_from_table (DEV ONLY: DOA, DOB)
Delete records from a table.
```
Parameters:
  - server_name: Must be DOA or DOB environment
  - database_name: Target database
  - table_name: Table name
  - where_clause: WHERE condition (REQUIRED)
```

### SQL Agent Job Operations

#### list_agent_jobs
List all SQL Server Agent jobs.
```
Parameters:
  - server_name: SQL Server instance
  - enabled_only: Show only enabled jobs (optional, default: false)
```

#### get_job_history
Get execution history for jobs.
```
Parameters:
  - server_name: SQL Server instance
  - job_name: Specific job (optional, default: all jobs)
  - last_n_runs: Number of runs (optional, default: 10)
  - date_from: Start date YYYY-MM-DD (optional)
  - date_to: End date YYYY-MM-DD (optional)
```

#### get_job_status
Get current status of a specific job.
```
Parameters:
  - server_name: SQL Server instance
  - job_name: Job name (required)
```

#### get_failed_jobs
Get jobs that failed recently.
```
Parameters:
  - server_name: SQL Server instance
  - hours: Lookback period (optional, default: 24)
```

### Instance Management Operations

#### get_instance_status
Get SQL Server instance information.
```
Parameters:
  - server_name: SQL Server instance
```

#### restart_sql_service
Restart SQL Server service (requires admin privileges).
```
Parameters:
  - server_name: SQL Server instance
  - service_name: Windows service name (optional, auto-detected)
  - force: Force restart (optional, default: false)
```

#### restart_agent_service
Restart SQL Server Agent service (requires admin privileges).
```
Parameters:
  - server_name: SQL Server instance
  - service_name: Windows service name (optional, auto-detected)
```

#### get_service_status
Get Windows service status.
```
Parameters:
  - server_name: SQL Server instance
  - service_type: 'engine' or 'agent' (optional, default: 'engine')
```

#### test_connection
Test connection and get server info.
```
Parameters:
  - server_name: SQL Server instance
  - database_name: Database (optional, default: master)
```

## Security

### Environment Restrictions
- **UPDATE, INSERT, DELETE** operations are **ONLY** allowed on DEV environments:
  - DOA (Development Environment A)
  - DOB (Development Environment B)
- All write operations on PRODUCTION servers will be **automatically blocked**
- WHERE clauses are **REQUIRED** for UPDATE and DELETE operations

### Authentication
- Uses Windows Authentication (Trusted Connection)
- Leverages current user's UCN credentials
- No passwords stored in configuration
- Permissions determined by SQL Server security settings

### Best Practices
- Always test queries on DEV before running on PROD
- Use WHERE clauses to limit result sets
- Service restarts require administrator privileges
- Review job history before making changes

## Usage Examples

### Using with OpenCode

```
User: List all tables in the DOA-SERVER\DEV database 'CustomerDB'
OpenCode: [Uses list_tables tool]

User: Show me the schema for the Users table
OpenCode: [Uses get_table_schema tool]

User: Update the status to 'active' for user ID 123
OpenCode: [Uses update_table tool with WHERE clause]
```

## Troubleshooting

### Connection Issues
- Verify ODBC Driver 17 is installed
- Check Windows Authentication is enabled
- Confirm network connectivity to SQL Server
- Verify user has appropriate SQL Server permissions

### Service Restart Failures
- Ensure OpenCode is running with administrator privileges
- Check Windows service names match SQL Server instance
- Verify no active connections are blocking restart

### Permission Errors
- Confirm user has appropriate database permissions
- Check SQL Server security settings
- Verify server is in correct environment (DOA/DOB for write operations)

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/
```

### Type Checking
```bash
mypy src/
```

## License

Proprietary - Internal Use Only

## Support

For issues or questions, contact your database administrator or IT support team.
