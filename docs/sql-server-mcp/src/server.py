"""
SQL Server Management MCP Server

Main entry point for the MCP server that provides SQL Server management capabilities.
"""
import asyncio
import logging
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from .tools import table_tools, job_tools, instance_tools
from .connection import SQLServerConnection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server instance
app = Server("sql-server-mcp")


# Tool definitions
TOOLS = [
    # Table query tools
    Tool(
        name="list_tables",
        description="List all tables in the dbo schema of a database",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {
                    "type": "string",
                    "description": "SQL Server instance name (e.g., 'localhost', 'SERVER\\INSTANCE')"
                },
                "database_name": {
                    "type": "string",
                    "description": "Target database name"
                }
            },
            "required": ["server_name", "database_name"]
        }
    ),
    Tool(
        name="get_table_schema",
        description="Get detailed schema information for a specific table",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "database_name": {"type": "string", "description": "Target database name"},
                "table_name": {"type": "string", "description": "Table name in dbo schema"}
            },
            "required": ["server_name", "database_name", "table_name"]
        }
    ),
    Tool(
        name="query_table",
        description="Execute a SELECT query on a dbo table",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "database_name": {"type": "string", "description": "Target database name"},
                "table_name": {"type": "string", "description": "Table name in dbo schema"},
                "columns": {"type": "string", "description": "Comma-separated column names (default: *)"},
                "where_clause": {"type": "string", "description": "WHERE condition without WHERE keyword"},
                "top_n": {"type": "integer", "description": "Maximum rows to return (default: 100)"}
            },
            "required": ["server_name", "database_name", "table_name"]
        }
    ),
    Tool(
        name="update_table",
        description="Execute UPDATE query on dbo table (DEV ONLY: DOA, DOB environments)",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance (must be DOA or DOB)"},
                "database_name": {"type": "string", "description": "Target database name"},
                "table_name": {"type": "string", "description": "Table name in dbo schema"},
                "set_clause": {"type": "string", "description": "SET clause (e.g., 'col1 = value1, col2 = value2')"},
                "where_clause": {"type": "string", "description": "WHERE condition (REQUIRED)"}
            },
            "required": ["server_name", "database_name", "table_name", "set_clause", "where_clause"]
        }
    ),
    Tool(
        name="insert_into_table",
        description="Execute INSERT query on dbo table (DEV ONLY: DOA, DOB environments)",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance (must be DOA or DOB)"},
                "database_name": {"type": "string", "description": "Target database name"},
                "table_name": {"type": "string", "description": "Table name in dbo schema"},
                "columns": {"type": "string", "description": "Comma-separated column names"},
                "values": {"type": "string", "description": "Comma-separated values"}
            },
            "required": ["server_name", "database_name", "table_name", "columns", "values"]
        }
    ),
    Tool(
        name="delete_from_table",
        description="Execute DELETE query on dbo table (DEV ONLY: DOA, DOB environments)",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance (must be DOA or DOB)"},
                "database_name": {"type": "string", "description": "Target database name"},
                "table_name": {"type": "string", "description": "Table name in dbo schema"},
                "where_clause": {"type": "string", "description": "WHERE condition (REQUIRED)"}
            },
            "required": ["server_name", "database_name", "table_name", "where_clause"]
        }
    ),
    # SQL Agent job tools
    Tool(
        name="list_agent_jobs",
        description="List all SQL Server Agent jobs",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "enabled_only": {"type": "boolean", "description": "Show only enabled jobs (default: false)"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="get_job_history",
        description="Get execution history for SQL Server Agent jobs",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "job_name": {"type": "string", "description": "Specific job name (optional)"},
                "last_n_runs": {"type": "integer", "description": "Number of recent runs (default: 10)"},
                "date_from": {"type": "string", "description": "Start date YYYY-MM-DD (optional)"},
                "date_to": {"type": "string", "description": "End date YYYY-MM-DD (optional)"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="get_job_status",
        description="Get current status of a specific SQL Server Agent job",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "job_name": {"type": "string", "description": "Job name"}
            },
            "required": ["server_name", "job_name"]
        }
    ),
    Tool(
        name="get_failed_jobs",
        description="Get jobs that failed in the last N hours",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "hours": {"type": "integer", "description": "Lookback period in hours (default: 24)"}
            },
            "required": ["server_name"]
        }
    ),
    # Instance management tools
    Tool(
        name="get_instance_status",
        description="Get SQL Server instance status and information",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="restart_sql_service",
        description="Restart SQL Server service (requires admin privileges)",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "service_name": {"type": "string", "description": "Windows service name (optional, auto-detected)"},
                "force": {"type": "boolean", "description": "Force restart (default: false)"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="restart_agent_service",
        description="Restart SQL Server Agent service (requires admin privileges)",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "service_name": {"type": "string", "description": "Windows service name (optional, auto-detected)"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="get_service_status",
        description="Get Windows service status for SQL Server",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "service_type": {"type": "string", "description": "Service type: 'engine' or 'agent' (default: 'engine')"}
            },
            "required": ["server_name"]
        }
    ),
    Tool(
        name="test_connection",
        description="Test connection to SQL Server and return server information",
        inputSchema={
            "type": "object",
            "properties": {
                "server_name": {"type": "string", "description": "SQL Server instance name"},
                "database_name": {"type": "string", "description": "Database name (default: master)"}
            },
            "required": ["server_name"]
        }
    )
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a tool with given arguments."""
    try:
        logger.info(f"Executing tool: {name} with arguments: {arguments}")

        # Table tools
        if name == "list_tables":
            result = table_tools.list_tables(
                arguments["server_name"],
                arguments["database_name"]
            )
        elif name == "get_table_schema":
            result = table_tools.get_table_schema(
                arguments["server_name"],
                arguments["database_name"],
                arguments["table_name"]
            )
        elif name == "query_table":
            result = table_tools.query_table(
                arguments["server_name"],
                arguments["database_name"],
                arguments["table_name"],
                arguments.get("columns"),
                arguments.get("where_clause"),
                arguments.get("top_n", 100)
            )
        elif name == "update_table":
            result = table_tools.update_table(
                arguments["server_name"],
                arguments["database_name"],
                arguments["table_name"],
                arguments["set_clause"],
                arguments["where_clause"]
            )
        elif name == "insert_into_table":
            result = table_tools.insert_into_table(
                arguments["server_name"],
                arguments["database_name"],
                arguments["table_name"],
                arguments["columns"],
                arguments["values"]
            )
        elif name == "delete_from_table":
            result = table_tools.delete_from_table(
                arguments["server_name"],
                arguments["database_name"],
                arguments["table_name"],
                arguments["where_clause"]
            )
        # Job tools
        elif name == "list_agent_jobs":
            result = job_tools.list_agent_jobs(
                arguments["server_name"],
                arguments.get("enabled_only", False)
            )
        elif name == "get_job_history":
            result = job_tools.get_job_history(
                arguments["server_name"],
                arguments.get("job_name"),
                arguments.get("last_n_runs", 10),
                arguments.get("date_from"),
                arguments.get("date_to")
            )
        elif name == "get_job_status":
            result = job_tools.get_job_status(
                arguments["server_name"],
                arguments["job_name"]
            )
        elif name == "get_failed_jobs":
            result = job_tools.get_failed_jobs(
                arguments["server_name"],
                arguments.get("hours", 24)
            )
        # Instance tools
        elif name == "get_instance_status":
            result = instance_tools.get_instance_status(arguments["server_name"])
        elif name == "restart_sql_service":
            result = instance_tools.restart_sql_service(
                arguments["server_name"],
                arguments.get("service_name"),
                arguments.get("force", False)
            )
        elif name == "restart_agent_service":
            result = instance_tools.restart_agent_service(
                arguments["server_name"],
                arguments.get("service_name")
            )
        elif name == "get_service_status":
            result = instance_tools.get_service_status(
                arguments["server_name"],
                arguments.get("service_type", "engine")
            )
        elif name == "test_connection":
            conn = SQLServerConnection(
                arguments["server_name"],
                arguments.get("database_name", "master")
            )
            result = conn.test_connection()
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Tool execution failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    logger.info("Starting SQL Server MCP Server")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
