# SQL Server Management MCP Server
## Complete Implementation and Usage Guide

**Version:** 1.0.0  
**Last Updated:** May 21, 2026  
**Document Type:** Technical Implementation Guide

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Prerequisites and Installation](#prerequisites-and-installation)
4. [Configuration](#configuration)
5. [Tool Reference](#tool-reference)
6. [Security and Access Control](#security-and-access-control)
7. [Usage Examples](#usage-examples)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Appendix](#appendix)

---

## Executive Summary

The SQL Server Management MCP (Model Context Protocol) Server is a comprehensive solution for managing Microsoft SQL Server instances through natural language interactions with AI assistants like OpenCode. This server provides secure, authenticated access to SQL Server operations including:

- **Database Querying**: Read-only access to dbo schema tables
- **Data Modification**: Controlled write operations (limited to DEV environments)
- **Job Monitoring**: SQL Server Agent job status and history tracking
- **Instance Management**: Server status monitoring and service control

### Key Features

- **Windows Authentication**: Seamless integration with existing UCN credentials
- **Environment Protection**: Automatic prevention of write operations on production servers
- **Comprehensive Logging**: Full audit trail of all operations
- **Error Handling**: Robust error management with detailed feedback

### Target Users

- Database Administrators
- DevOps Engineers
- Data Analysts
- Support Engineers

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         OpenCode                            │
│                      (AI Assistant)                         │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP Protocol
                     │
┌────────────────────┴────────────────────────────────────────┐
│              SQL Server MCP Server                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tool Handler (server.py)                            │  │
│  └───┬──────────────────────┬───────────────────┬───────┘  │
│      │                      │                   │           │
│  ┌───┴────────┐  ┌──────────┴─────────┐  ┌─────┴──────┐   │
│  │Table Tools │  │   Job Tools        │  │Instance    │   │
│  │            │  │                    │  │Tools       │   │
│  └───┬────────┘  └──────────┬─────────┘  └─────┬──────┘   │
│      │                      │                   │           │
│  ┌───┴──────────────────────┴───────────────────┴───────┐  │
│  │         Connection Manager (connection.py)           │  │
│  └───────────────────────────┬──────────────────────────┘  │
└──────────────────────────────┼─────────────────────────────┘
                               │ Windows Auth
                               │ (pyodbc)
┌──────────────────────────────┴─────────────────────────────┐
│                    SQL Server Instances                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ DOA-SERVER   │  │ DOB-SERVER   │  │ PROD-SERVER     │ │
│  │ (Dev Env)    │  │ (Dev Env)    │  │ (Protected)     │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Runtime | Python | 3.9+ | Core execution environment |
| MCP SDK | mcp | 0.9.0+ | Protocol implementation |
| SQL Driver | pyodbc | 5.0.0+ | Database connectivity |
| Windows API | pywin32 | 306+ | Service management |
| ODBC Driver | Microsoft ODBC Driver 17 | Latest | SQL Server communication |

### File Structure

```
sql-server-mcp/
├── src/
│   ├── __init__.py                # Package initialization
│   ├── server.py                  # Main MCP server and tool registration
│   ├── connection.py              # Connection management and auth
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── table_tools.py         # Table operations (query/update/insert/delete)
│   │   ├── job_tools.py           # SQL Agent job operations
│   │   └── instance_tools.py      # Instance and service management
│   └── utils/
│       └── __init__.py
├── docs/
│   └── COMPLETE_GUIDE.md          # This document
├── pyproject.toml                 # Python project configuration
└── README.md                      # Quick start guide
```

---

## Prerequisites and Installation

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows Server 2016+ or Windows 10+
- **Python Version**: 3.9 or higher
- **Memory**: 2 GB RAM
- **Disk Space**: 100 MB for MCP server + dependencies

#### Network Requirements
- Network connectivity to target SQL Server instances
- Appropriate firewall rules for SQL Server ports (default: 1433)
- Windows domain authentication configured

### Software Dependencies

#### 1. Microsoft ODBC Driver 17 for SQL Server

**Installation Steps:**

1. Download from Microsoft: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
2. Run the installer: `msodbcsql.msi`
3. Accept license terms
4. Complete installation

**Verification:**
```powershell
# Check installed ODBC drivers
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
```

Expected output:
```
Name                           Platform      Version
----                           --------      -------
ODBC Driver 17 for SQL Server  64-bit        17.x.x.x
```

#### 2. Python 3.9+

**Check Python version:**
```powershell
python --version
```

If Python is not installed:
1. Download from python.org
2. Ensure "Add Python to PATH" is checked during installation
3. Verify installation: `python --version`

#### 3. Python Dependencies

**Installation Command:**
```powershell
cd C:\path\to\sql-server-mcp
pip install -e .
```

**Dependencies installed:**
- `mcp>=0.9.0` - MCP protocol implementation
- `pyodbc>=5.0.0` - SQL Server connectivity
- `pywin32>=306` - Windows service management

**Verify installation:**
```powershell
pip list | Select-String "mcp|pyodbc|pywin32"
```

### SQL Server Permissions

The Windows user running OpenCode needs the following SQL Server permissions:

#### Minimum Permissions (Read-Only)
```sql
-- Grant connect permission
USE master;
GRANT CONNECT SQL TO [DOMAIN\Username];

-- Grant database access
USE [YourDatabase];
CREATE USER [DOMAIN\Username] FOR LOGIN [DOMAIN\Username];
ALTER ROLE db_datareader ADD MEMBER [DOMAIN\Username];

-- Grant msdb access for job monitoring
USE msdb;
CREATE USER [DOMAIN\Username] FOR LOGIN [DOMAIN\Username];
ALTER ROLE SQLAgentReaderRole ADD MEMBER [DOMAIN\Username];
```

#### Additional Permissions for DEV Environments
```sql
-- Grant write permissions (DOA/DOB only)
USE [YourDatabase];
ALTER ROLE db_datawriter ADD MEMBER [DOMAIN\Username];
```

#### Service Management Permissions
- Windows Administrator privileges required for service restart operations
- Run OpenCode as Administrator when service management is needed

---

## Configuration

### OpenCode Integration

#### Configuration File Location

Choose one of:
- **User-level**: `C:\Users\<username>\.config\opencode\config.json`
- **Workspace-level**: `<workspace>\.opencode\config.json`

#### Configuration Template

```json
{
  "mcpServers": {
    "sql-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:/Users/ramiro.maceda/sql-server-mcp",
      "env": {
        "PYTHONPATH": "C:/Users/ramiro.maceda/sql-server-mcp",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Configuration Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| `command` | Python executable | Yes | `"python"` or `"python3"` |
| `args` | Module to run | Yes | `["-m", "src.server"]` |
| `cwd` | Working directory | Yes | Full path to sql-server-mcp |
| `env.PYTHONPATH` | Python path | Recommended | Same as cwd |
| `env.LOG_LEVEL` | Logging level | Optional | `"INFO"`, `"DEBUG"`, `"ERROR"` |

### Environment Detection

The MCP server automatically detects the environment based on server naming conventions:

| Server Name Pattern | Detected Environment | Write Operations Allowed |
|---------------------|---------------------|-------------------------|
| Contains "DOA" | Development A (DOA) | ✅ Yes |
| Contains "DOB" | Development B (DOB) | ✅ Yes |
| Contains "PROD", "PRD", "PRODUCTION" | Production | ❌ No |
| Other | Unknown | ❌ No |

**Examples:**
- `DOA-SQL-SERVER\INSTANCE` → DOA (write allowed)
- `SQL-DOB-01` → DOB (write allowed)
- `PROD-SQL-SERVER` → Production (write blocked)
- `MY-SQL-SERVER` → Unknown (write blocked)

---

## Tool Reference

### Table Operations

#### 1. list_tables

**Purpose**: List all tables in the dbo schema of a database.

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB"
}
```

**Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table_count": 15,
  "tables": [
    {
      "table_name": "Users",
      "schema_name": "dbo",
      "row_count": 1250,
      "total_space_kb": 2048
    },
    {
      "table_name": "Orders",
      "schema_name": "dbo",
      "row_count": 5678,
      "total_space_kb": 8192
    }
  ]
}
```

**Use Cases:**
- Database discovery
- Table inventory
- Storage analysis
- Documentation generation

---

#### 2. get_table_schema

**Purpose**: Get detailed schema information including columns, data types, and constraints.

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Users"
}
```

**Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table": "Users",
  "columns": [
    {
      "column_name": "UserId",
      "data_type": "int",
      "max_length": 4,
      "precision": 10,
      "scale": 0,
      "is_nullable": false,
      "is_identity": true,
      "is_primary_key": true
    },
    {
      "column_name": "Username",
      "data_type": "nvarchar",
      "max_length": 100,
      "is_nullable": false,
      "is_identity": false,
      "is_primary_key": false
    }
  ]
}
```

**Use Cases:**
- Understanding table structure
- Planning data migrations
- Generating documentation
- Validating data types before queries

---

#### 3. query_table

**Purpose**: Execute SELECT queries on dbo schema tables with filtering and limiting.

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Users",
  "columns": "UserId, Username, Email, CreatedDate",
  "where_clause": "Status = 'Active' AND CreatedDate >= '2026-01-01'",
  "top_n": 50
}
```

**Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table": "Users",
  "row_count": 23,
  "rows": [
    {
      "UserId": 101,
      "Username": "jdoe",
      "Email": "jdoe@example.com",
      "CreatedDate": "2026-01-15T10:30:00"
    },
    {
      "UserId": 102,
      "Username": "asmith",
      "Email": "asmith@example.com",
      "CreatedDate": "2026-01-20T14:45:00"
    }
  ]
}
```

**Query Examples:**

Simple query (all columns):
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Users"
}
```

With WHERE clause:
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Orders",
  "where_clause": "OrderDate >= '2026-01-01' AND Status = 'Pending'"
}
```

Specific columns:
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Products",
  "columns": "ProductId, ProductName, Price"
}
```

**Use Cases:**
- Data analysis
- Report generation
- Data validation
- Troubleshooting

---

#### 4. update_table (DEV ONLY)

**Purpose**: Update records in a table (restricted to DOA and DOB environments).

**⚠️ RESTRICTIONS:**
- Only works on DOA or DOB servers
- WHERE clause is REQUIRED
- Automatically blocked on production servers

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Users",
  "set_clause": "Status = 'Inactive', ModifiedDate = GETDATE()",
  "where_clause": "UserId = 101"
}
```

**Success Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table": "Users",
  "rows_affected": 1,
  "operation": "UPDATE"
}
```

**Error Response (Production Server):**
```json
{
  "success": false,
  "error": "UPDATE operations are only allowed on DEV environments (DOA, DOB). Server 'PROD-SERVER' is not a dev environment.",
  "server": "PROD-SERVER"
}
```

**Error Response (Missing WHERE):**
```json
{
  "success": false,
  "error": "WHERE clause is required for UPDATE operations to prevent accidental full table updates"
}
```

**Use Cases:**
- Data corrections in dev/test
- Status updates
- Test data preparation
- Bug fixing

---

#### 5. insert_into_table (DEV ONLY)

**Purpose**: Insert new records into a table (restricted to DOA and DOB environments).

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "Users",
  "columns": "Username, Email, Status, CreatedDate",
  "values": "'testuser', 'test@example.com', 'Active', GETDATE()"
}
```

**Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table": "Users",
  "rows_affected": 1,
  "operation": "INSERT"
}
```

**Use Cases:**
- Test data creation
- Manual data entry
- Data migration testing
- Development setup

---

#### 6. delete_from_table (DEV ONLY)

**Purpose**: Delete records from a table (restricted to DOA and DOB environments).

**⚠️ RESTRICTIONS:**
- Only works on DOA or DOB servers
- WHERE clause is REQUIRED
- Automatically blocked on production servers

**Parameters:**
```json
{
  "server_name": "DOB-SERVER\\INSTANCE",
  "database_name": "CustomerDB",
  "table_name": "TestData",
  "where_clause": "CreatedDate < '2026-01-01' AND IsTestData = 1"
}
```

**Response:**
```json
{
  "success": true,
  "server": "DOB-SERVER\\INSTANCE",
  "database": "CustomerDB",
  "table": "TestData",
  "rows_affected": 125,
  "operation": "DELETE"
}
```

**Use Cases:**
- Cleanup of test data
- Data archiving preparation
- Development environment maintenance
- Bug testing

---

### SQL Agent Job Operations

#### 7. list_agent_jobs

**Purpose**: List all SQL Server Agent jobs with current status.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "enabled_only": true
}
```

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "job_count": 12,
  "jobs": [
    {
      "job_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
      "job_name": "Daily Backup Job",
      "enabled": true,
      "description": "Full backup of all databases",
      "owner": "DOMAIN\\sqladmin",
      "date_created": "2025-01-15T10:00:00",
      "date_modified": "2026-03-10T15:30:00",
      "current_status": "Idle"
    },
    {
      "job_id": "B2C3D4E5-F6G7-8901-BCDE-F12345678901",
      "job_name": "Hourly Data Sync",
      "enabled": true,
      "description": "Sync data from source system",
      "owner": "DOMAIN\\etluser",
      "date_created": "2025-02-01T09:00:00",
      "date_modified": "2026-04-05T11:20:00",
      "current_status": "Running"
    }
  ]
}
```

**Use Cases:**
- Job inventory
- Monitoring job status
- Finding disabled jobs
- Ownership review

---

#### 8. get_job_history

**Purpose**: Retrieve execution history for SQL Server Agent jobs.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "job_name": "Daily Backup Job",
  "last_n_runs": 10
}
```

**Alternative - Date Range:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "date_from": "2026-05-01",
  "date_to": "2026-05-21",
  "last_n_runs": 100
}
```

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "job_name": "Daily Backup Job",
  "history_count": 10,
  "history": [
    {
      "job_name": "Daily Backup Job",
      "step_id": 0,
      "step_name": "(Job outcome)",
      "run_date": 20260521,
      "run_time": 20000,
      "run_status": "Succeeded",
      "run_duration": 3245,
      "message": "The job succeeded. The Job was invoked by Schedule 1 (Daily Schedule).",
      "retries_attempted": 0,
      "run_datetime": "2026-05-21T02:00:00"
    },
    {
      "job_name": "Daily Backup Job",
      "step_id": 0,
      "step_name": "(Job outcome)",
      "run_date": 20260520,
      "run_time": 20000,
      "run_status": "Succeeded",
      "run_duration": 3189,
      "message": "The job succeeded.",
      "retries_attempted": 0,
      "run_datetime": "2026-05-20T02:00:00"
    }
  ]
}
```

**Run Status Values:**
- `Succeeded` - Job completed successfully
- `Failed` - Job failed
- `Retry` - Job was retried
- `Canceled` - Job was canceled
- `In Progress` - Job is currently running

**Use Cases:**
- Troubleshooting job failures
- Performance analysis
- Audit compliance
- Historical reporting

---

#### 9. get_job_status

**Purpose**: Get current status and next scheduled run for a specific job.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "job_name": "Daily Backup Job"
}
```

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "job_status": {
    "job_name": "Daily Backup Job",
    "enabled": true,
    "description": "Full backup of all databases",
    "current_status": "Idle",
    "start_execution_date": null,
    "last_executed_step_id": 1,
    "last_executed_step_date": "2026-05-21T02:54:23",
    "next_run_date": 20260522,
    "next_run_time": 20000,
    "next_scheduled_run": "2026-05-22T02:00:00",
    "last_run_date": 20260521,
    "last_run_time": 20000,
    "last_run_status": "Succeeded",
    "last_run_duration": 3245
  }
}
```

**Use Cases:**
- Real-time monitoring
- Scheduling verification
- Quick health check
- On-call support

---

#### 10. get_failed_jobs

**Purpose**: Get all jobs that failed in the specified time window.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "hours": 24
}
```

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "lookback_hours": 24,
  "failed_job_count": 2,
  "failed_jobs": [
    {
      "job_name": "Data Import Job",
      "step_id": 0,
      "step_name": "(Job outcome)",
      "run_date": 20260521,
      "run_time": 30000,
      "run_duration": 45,
      "message": "The job failed. Unable to connect to source database. Timeout expired.",
      "run_datetime": "2026-05-21T03:00:00"
    },
    {
      "job_name": "Report Generation",
      "step_id": 0,
      "step_name": "(Job outcome)",
      "run_date": 20260520,
      "run_time": 180000,
      "run_duration": 12,
      "message": "The job failed. Insufficient permissions on target folder.",
      "run_datetime": "2026-05-20T18:00:00"
    }
  ]
}
```

**Use Cases:**
- Proactive monitoring
- Alert investigation
- Daily health checks
- Incident response

---

### Instance Management Operations

#### 11. get_instance_status

**Purpose**: Get comprehensive SQL Server instance information and health status.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE"
}
```

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "status": "Online",
  "instance_info": {
    "version": "Microsoft SQL Server 2019 (RTM-CU15) - 15.0.4198.2 (X64)",
    "server_name": "PROD-SERVER\\INSTANCE",
    "product_version": "15.0.4198.2",
    "product_level": "RTM",
    "edition": "Enterprise Edition: Core-based Licensing (64-bit)",
    "is_clustered": false,
    "is_hadr_enabled": true,
    "sql_server_start_time": "2026-04-15T08:30:15"
  },
  "database_count": 25,
  "user_connections": 47
}
```

**Offline Response:**
```json
{
  "success": false,
  "server": "PROD-SERVER\\INSTANCE",
  "status": "Offline or Inaccessible",
  "error": "Unable to connect to server. Timeout expired."
}
```

**Use Cases:**
- Health monitoring
- Version verification
- Capacity planning
- Uptime tracking

---

#### 12. restart_sql_service

**Purpose**: Restart the SQL Server database engine service.

**⚠️ REQUIRES:** Administrator privileges

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "force": false
}
```

**Auto-detected service name:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE"
}
```
- Default instance → `MSSQLSERVER`
- Named instance → `MSSQL$INSTANCE`

**Manual service name:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "service_name": "MSSQL$MYINSTANCE",
  "force": true
}
```

**Success Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "service_name": "MSSQL$INSTANCE",
  "operation": "restart",
  "message": "Service 'MSSQL$INSTANCE' restarted successfully"
}
```

**Error Response (No Admin):**
```json
{
  "success": false,
  "error": "Access denied",
  "note": "Ensure the application is running with administrator privileges"
}
```

**Use Cases:**
- Configuration changes requiring restart
- Performance issue resolution
- Maintenance procedures
- Emergency response

---

#### 13. restart_agent_service

**Purpose**: Restart the SQL Server Agent service.

**⚠️ REQUIRES:** Administrator privileges

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE"
}
```

**Service name auto-detection:**
- Default instance → `SQLSERVERAGENT`
- Named instance → `SQLAgent$INSTANCE`

**Response:**
```json
{
  "success": true,
  "server": "DOA-SERVER\\INSTANCE",
  "service_name": "SQLAgent$INSTANCE",
  "operation": "restart",
  "message": "Agent service 'SQLAgent$INSTANCE' restarted successfully"
}
```

**Use Cases:**
- Job schedule updates
- Agent configuration changes
- Troubleshooting job execution
- Maintenance procedures

---

#### 14. get_service_status

**Purpose**: Check Windows service status for SQL Server or Agent.

**Parameters:**
```json
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "service_type": "engine"
}
```

**Service Types:**
- `engine` - SQL Server Database Engine
- `agent` - SQL Server Agent

**Response:**
```json
{
  "success": true,
  "server": "PROD-SERVER\\INSTANCE",
  "service_name": "MSSQL$INSTANCE",
  "service_type": "engine",
  "status": "Running",
  "status_code": 4
}
```

**Status Values:**
- `Running` (4) - Service is running
- `Stopped` (1) - Service is stopped
- `Starting` (2) - Service is starting
- `Stopping` (3) - Service is stopping
- `Paused` (7) - Service is paused

**Use Cases:**
- Pre-restart validation
- Monitoring automation
- Health checks
- Troubleshooting

---

#### 15. test_connection

**Purpose**: Test connectivity and authentication to SQL Server.

**Parameters:**
```json
{
  "server_name": "DOA-SERVER\\INSTANCE",
  "database_name": "master"
}
```

**Success Response:**
```json
{
  "status": "connected",
  "server_info": {
    "version": "Microsoft SQL Server 2019...",
    "server_name": "DOA-SERVER\\INSTANCE",
    "database_name": "master",
    "current_user": "DOMAIN\\username"
  }
}
```

**Failure Response:**
```json
{
  "status": "failed",
  "error": "Login timeout expired"
}
```

**Use Cases:**
- Initial setup verification
- Troubleshooting connectivity
- Permission validation
- Network testing

---

## Security and Access Control

### Authentication Model

#### Windows Authentication Flow

```
User runs OpenCode
    ↓
OpenCode starts MCP Server
    ↓
MCP Server uses current Windows user context
    ↓
pyodbc connects with Trusted_Connection=yes
    ↓
SQL Server validates Windows credentials
    ↓
SQL Server applies role-based permissions
    ↓
Operations execute with user's SQL Server permissions
```

### Environment-Based Access Control

#### Write Operation Protection

**Allowed Environments:**
- DOA (Development Environment A)
- DOB (Development Environment B)

**Blocked Environments:**
- Production (any server with PROD, PRD, or PRODUCTION in name)
- Unknown environments

**Implementation:**
```python
def is_dev_environment(server_name: str) -> bool:
    server_upper = server_name.upper()
    if "DOA" in server_upper or "DOB" in server_upper:
        return True
    return False
```

**Bypass Protection:**
There is **NO** way to bypass this protection. Write operations on production servers are hard-coded to fail.

### SQL Injection Prevention

All queries use **parameterized statements**:

```python
# SAFE - Parameterized
cursor.execute("SELECT * FROM dbo.Users WHERE UserId = ?", (user_id,))

# UNSAFE - String concatenation (NOT USED)
cursor.execute(f"SELECT * FROM dbo.Users WHERE UserId = {user_id}")
```

### Audit Logging

All operations are logged with:
- Timestamp
- User context
- Server/database
- Operation type
- Parameters
- Success/failure
- Error details (if any)

**Log Location:** 
Console output (can be redirected to file)

**Log Format:**
```
2026-05-21 14:30:15 - connection - INFO - Connecting to PROD-SERVER\INSTANCE/CustomerDB
2026-05-21 14:30:16 - table_tools - INFO - Query executed successfully, returned 25 rows
2026-05-21 14:30:16 - connection - INFO - Connection closed to PROD-SERVER\INSTANCE/CustomerDB
```

---

## Usage Examples

### Example 1: Daily Job Failure Investigation

**Scenario:** Support receives alert that backup jobs failed overnight.

**Step 1: Check failed jobs in last 24 hours**
```
User: Show me all SQL Server Agent jobs that failed in the last 24 hours on PROD-SERVER\INSTANCE

OpenCode executes: get_failed_jobs
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "hours": 24
}

Result: 3 jobs failed
- Daily Backup Job (Failed at 02:00:00)
- Transaction Log Backup (Failed at 02:15:00)  
- Index Maintenance (Failed at 03:00:00)
```

**Step 2: Get detailed history for specific job**
```
User: Show me the detailed history for the Daily Backup Job

OpenCode executes: get_job_history
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "job_name": "Daily Backup Job",
  "last_n_runs": 10
}

Result: Last 10 runs shown
- Today: Failed (Disk full error)
- Yesterday: Succeeded
- Day before: Succeeded
```

**Step 3: Check instance status**
```
User: What's the current status of PROD-SERVER\INSTANCE?

OpenCode executes: get_instance_status
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE"
}

Result: Instance Online, 47 user connections, version 15.0.4198.2
```

**Resolution:** Disk space issue identified. Escalate to storage team.

---

### Example 2: Development Data Setup

**Scenario:** Developer needs to create test data in DOA environment.

**Step 1: List available tables**
```
User: List all tables in DOA-SERVER\DEV database TestDB

OpenCode executes: list_tables
Parameters:
{
  "server_name": "DOA-SERVER\\DEV",
  "database_name": "TestDB"
}

Result: 8 tables found including Users, Orders, Products
```

**Step 2: Check table structure**
```
User: Show me the schema for the Users table

OpenCode executes: get_table_schema
Parameters:
{
  "server_name": "DOA-SERVER\\DEV",
  "database_name": "TestDB",
  "table_name": "Users"
}

Result: Columns shown - UserId (int, identity), Username (nvarchar), Email (nvarchar), Status (varchar)
```

**Step 3: Insert test users**
```
User: Insert a test user with username 'testuser1' and email 'test1@example.com'

OpenCode executes: insert_into_table
Parameters:
{
  "server_name": "DOA-SERVER\\DEV",
  "database_name": "TestDB",
  "table_name": "Users",
  "columns": "Username, Email, Status, CreatedDate",
  "values": "'testuser1', 'test1@example.com', 'Active', GETDATE()"
}

Result: 1 row inserted successfully
```

**Step 4: Verify insertion**
```
User: Show me the user we just created

OpenCode executes: query_table
Parameters:
{
  "server_name": "DOA-SERVER\\DEV",
  "database_name": "TestDB",
  "table_name": "Users",
  "where_clause": "Username = 'testuser1'"
}

Result: User record displayed with UserId = 501
```

---

### Example 3: Production Monitoring

**Scenario:** DBA wants to monitor job health across multiple servers.

**Step 1: Check all jobs on primary server**
```
User: List all enabled SQL Agent jobs on PROD-SERVER\INSTANCE

OpenCode executes: list_agent_jobs
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "enabled_only": true
}

Result: 15 enabled jobs listed
```

**Step 2: Check status of critical job**
```
User: What's the status of the "Daily Backup Job"?

OpenCode executes: get_job_status
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "job_name": "Daily Backup Job"
}

Result: Status = Idle, Last Run = Succeeded, Next Run = 2026-05-22 02:00:00
```

**Step 3: Query data for validation**
```
User: Show me the last 10 records from the BackupHistory table

OpenCode executes: query_table
Parameters:
{
  "server_name": "PROD-SERVER\\INSTANCE",
  "database_name": "DBA_Tools",
  "table_name": "BackupHistory",
  "top_n": 10
}

Result: Recent backups displayed with timestamps and sizes
```

---

### Example 4: Incident Response

**Scenario:** Production issue requires service restart.

**⚠️ Important:** Requires admin privileges

**Step 1: Check current service status**
```
User: Check the SQL Server service status on DOB-SERVER\TEST

OpenCode executes: get_service_status
Parameters:
{
  "server_name": "DOB-SERVER\\TEST",
  "service_type": "engine"
}

Result: Status = Running, but high CPU reported elsewhere
```

**Step 2: Restart SQL Server service**
```
User: Restart the SQL Server service on DOB-SERVER\TEST

OpenCode executes: restart_sql_service
Parameters:
{
  "server_name": "DOB-SERVER\\TEST",
  "force": false
}

Result: Service restarted successfully
Time taken: ~45 seconds
```

**Step 3: Verify instance is back online**
```
User: Test connection to DOB-SERVER\TEST

OpenCode executes: test_connection
Parameters:
{
  "server_name": "DOB-SERVER\\TEST"
}

Result: Connected successfully, instance online
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Connection Timeout

**Error Message:**
```
Unable to connect to server. Timeout expired. [Microsoft][ODBC Driver 17 for SQL Server]
```

**Possible Causes:**
1. Server is offline
2. Network connectivity issue
3. Firewall blocking connection
4. Incorrect server name

**Solutions:**

1. **Verify server is online:**
   ```powershell
   Test-NetConnection PROD-SERVER -Port 1433
   ```

2. **Check SQL Server service:**
   ```powershell
   Get-Service MSSQLSERVER
   ```

3. **Verify server name:**
   - Check for typos
   - Use `ServerName\InstanceName` format for named instances
   - Use just `ServerName` for default instances

4. **Test connectivity:**
   ```powershell
   sqlcmd -S PROD-SERVER\INSTANCE -E -Q "SELECT @@VERSION"
   ```

---

#### Issue 2: Authentication Failed

**Error Message:**
```
Login failed for user 'DOMAIN\username'. [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]
```

**Possible Causes:**
1. User not granted SQL Server access
2. Windows Authentication not enabled
3. Wrong domain or username

**Solutions:**

1. **Grant SQL Server login:**
   ```sql
   USE master;
   CREATE LOGIN [DOMAIN\username] FROM WINDOWS;
   ```

2. **Grant database access:**
   ```sql
   USE YourDatabase;
   CREATE USER [DOMAIN\username] FOR LOGIN [DOMAIN\username];
   ALTER ROLE db_datareader ADD MEMBER [DOMAIN\username];
   ```

3. **Verify authentication mode:**
   ```sql
   SELECT SERVERPROPERTY('IsIntegratedSecurityOnly') AS WindowsAuthOnly;
   -- Should return 1 for Windows Auth
   ```

---

#### Issue 3: ODBC Driver Not Found

**Error Message:**
```
[Microsoft][ODBC Driver Manager] Data source name not found and no default driver specified
```

**Solutions:**

1. **Install ODBC Driver 17:**
   - Download from Microsoft
   - Install using `msodbcsql.msi`

2. **Verify installation:**
   ```powershell
   Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
   ```

3. **Update connection string if needed:**
   - ODBC Driver 17 for SQL Server (recommended)
   - ODBC Driver 13 for SQL Server (older)
   - SQL Server Native Client 11.0 (legacy)

---

#### Issue 4: Permission Denied on Write Operations

**Error Message:**
```
UPDATE operations are only allowed on DEV environments (DOA, DOB). Server 'PROD-SERVER' is not a dev environment.
```

**Explanation:**
This is **by design** for security. Write operations only work on DOA and DOB servers.

**Solutions:**

1. **Use DEV server:**
   - Change server_name to DOA-SERVER or DOB-SERVER
   - Verify server name contains "DOA" or "DOB"

2. **If you need to update production:**
   - Connect directly to SQL Server
   - Use SQL Server Management Studio (SSMS)
   - Follow change management procedures
   - **DO NOT** modify the MCP server code to bypass this

---

#### Issue 5: Service Restart Fails

**Error Message:**
```
Access denied. Ensure the application is running with administrator privileges.
```

**Solutions:**

1. **Run OpenCode as Administrator:**
   - Right-click OpenCode
   - Select "Run as Administrator"
   - Try service restart again

2. **Verify service permissions:**
   ```powershell
   # Check if user is admin
   ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
   ```

3. **Alternative - Use Services console:**
   - Open `services.msc`
   - Find SQL Server service
   - Right-click → Restart

---

#### Issue 6: MCP Server Not Starting

**Error Message:**
```
Failed to start MCP server 'sql-server'
```

**Solutions:**

1. **Check Python installation:**
   ```powershell
   python --version
   pip list | Select-String "mcp|pyodbc|pywin32"
   ```

2. **Verify configuration:**
   - Check config.json syntax (valid JSON)
   - Verify 'cwd' path exists
   - Ensure Python executable is in PATH

3. **Check logs:**
   - OpenCode console output
   - Look for Python errors
   - Verify import statements work

4. **Test server manually:**
   ```powershell
   cd C:\path\to\sql-server-mcp
   python -m src.server
   # Should not throw errors
   ```

---

#### Issue 7: Slow Query Performance

**Symptoms:**
- Queries taking long time
- Timeout errors
- High wait times

**Solutions:**

1. **Limit result set:**
   ```json
   {
     "top_n": 100  // Instead of 10000
   }
   ```

2. **Use WHERE clause:**
   ```json
   {
     "where_clause": "CreatedDate >= '2026-01-01'"  // Filter data
   }
   ```

3. **Select specific columns:**
   ```json
   {
     "columns": "UserId, Username"  // Not SELECT *
   }
   ```

4. **Check SQL Server:**
   - High CPU or memory usage
   - Missing indexes
   - Long-running queries

---

## Best Practices

### Query Optimization

#### 1. Always Use Filters
```json
// ❌ BAD - Returns entire table
{
  "table_name": "Users"
}

// ✅ GOOD - Filtered result
{
  "table_name": "Users",
  "where_clause": "Status = 'Active' AND LastLoginDate >= '2026-01-01'",
  "top_n": 100
}
```

#### 2. Select Specific Columns
```json
// ❌ BAD - Returns all columns
{
  "columns": "*"
}

// ✅ GOOD - Only needed columns
{
  "columns": "UserId, Username, Email"
}
```

#### 3. Limit Result Sets
```json
{
  "top_n": 100  // Reasonable limit
}
```

### Data Modification Safety

#### 1. Always Use WHERE for Updates
```json
// ❌ BAD - Blocked by system
{
  "set_clause": "Status = 'Inactive'",
  "where_clause": ""  // Missing!
}

// ✅ GOOD - Specific record
{
  "set_clause": "Status = 'Inactive'",
  "where_clause": "UserId = 101"
}
```

#### 2. Test in DEV First
```
1. Test query on DOA-SERVER
2. Verify results
3. Document expected changes
4. Apply to DOB-SERVER
5. Final verification
6. Apply to PROD (if needed, via SSMS)
```

#### 3. Preview Before Modifying
```json
// Step 1: SELECT to preview
{
  "tool": "query_table",
  "where_clause": "UserId = 101"
}

// Step 2: UPDATE with same WHERE clause
{
  "tool": "update_table",
  "set_clause": "Status = 'Inactive'",
  "where_clause": "UserId = 101"
}
```

### Job Monitoring

#### 1. Regular Health Checks
```
Daily: get_failed_jobs (hours: 24)
Weekly: get_job_history (all jobs, last 7 days)
Monthly: Review all job schedules
```

#### 2. Proactive Monitoring
```
- Check failed jobs before business hours
- Monitor long-running jobs
- Validate backup completions
- Review job performance trends
```

#### 3. Alert Response
```
1. get_failed_jobs - Identify failures
2. get_job_history - Review pattern
3. get_instance_status - Check server health
4. Escalate if needed
```

### Service Management

#### 1. Plan Restarts
```
- Schedule during maintenance window
- Notify stakeholders
- Check for active connections
- Verify backup status
- Document reason for restart
```

#### 2. Post-Restart Validation
```
1. test_connection - Verify connectivity
2. get_instance_status - Check health
3. get_service_status - Confirm running
4. list_agent_jobs - Verify jobs started
5. Review error logs
```

### Security Practices

#### 1. Use Least Privilege
```
- Grant only needed permissions
- Use read-only access when possible
- Restrict write access to DEV only
- Regular permission audits
```

#### 2. Never Bypass Protection
```
// ❌ NEVER modify environment detection
// ❌ NEVER remove WHERE clause requirements
// ❌ NEVER disable parameterization
```

#### 3. Audit Regularly
```
- Review logs weekly
- Monitor unusual activity
- Track permission changes
- Document all write operations
```

---

## Appendix

### A. Error Code Reference

| Error Code | Description | Action |
|------------|-------------|--------|
| 08001 | Connection failed | Check network/firewall |
| 28000 | Login failed | Verify permissions |
| 42000 | Syntax error | Check SQL syntax |
| HYT00 | Timeout | Optimize query or increase timeout |
| 23000 | Constraint violation | Check FK/PK constraints |

### B. SQL Server Edition Comparison

| Edition | Usage | MCP Support |
|---------|-------|-------------|
| Express | Dev/Test | ✅ Full |
| Standard | Small/Medium | ✅ Full |
| Enterprise | Large/Critical | ✅ Full |
| Developer | Development | ✅ Full |

### C. Default Port Numbers

| Service | Default Port |
|---------|--------------|
| SQL Server | 1433 |
| SQL Browser | 1434 |
| Named Instance | Dynamic |

### D. Performance Tuning Tips

1. **Index Usage:**
   - Ensure WHERE clause uses indexed columns
   - Review execution plans
   - Monitor missing indexes

2. **Query Optimization:**
   - Avoid SELECT *
   - Use TOP clause
   - Filter early in WHERE

3. **Connection Management:**
   - Connection pooling automatic
   - Timeout: 30 seconds (configurable)
   - Max connections: SQL Server setting

### E. Glossary

| Term | Definition |
|------|------------|
| MCP | Model Context Protocol |
| UCN | User Credential Name (Windows) |
| DBO | Database Owner schema |
| ODBC | Open Database Connectivity |
| pyodbc | Python ODBC library |

### F. Additional Resources

1. **SQL Server Documentation:**
   https://docs.microsoft.com/sql/

2. **MCP Protocol:**
   https://modelcontextprotocol.io/

3. **pyodbc Documentation:**
   https://github.com/mkleehammer/pyodbc

4. **OpenCode Documentation:**
   https://opencode.ai/docs

### G. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-21 | Initial release |

### H. Support Contact

For technical support:
- Database Team: dba-team@company.com
- IT Support: it-support@company.com
- On-call: See internal wiki

---

**Document End**

*This guide is maintained by the Database Administration team. Last updated: May 21, 2026*
