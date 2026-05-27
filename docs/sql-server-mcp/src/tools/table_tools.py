"""
Tools for querying and managing SQL Server tables.
"""
from typing import Any, Dict, List, Optional
import logging
from ..connection import SQLServerConnection, is_dev_environment

logger = logging.getLogger(__name__)


def list_tables(server_name: str, database_name: str) -> Dict[str, Any]:
    """
    List all tables in the dbo schema.

    Args:
        server_name: SQL Server instance name
        database_name: Target database

    Returns:
        Dictionary with list of tables and metadata
    """
    try:
        conn = SQLServerConnection(server_name, database_name)

        query = """
        SELECT 
            t.name as table_name,
            SCHEMA_NAME(t.schema_id) as schema_name,
            p.rows as row_count,
            SUM(a.total_pages) * 8 as total_space_kb
        FROM 
            sys.tables t
        INNER JOIN      
            sys.indexes i ON t.object_id = i.object_id
        INNER JOIN 
            sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
        INNER JOIN 
            sys.allocation_units a ON p.partition_id = a.container_id
        WHERE 
            t.schema_id = SCHEMA_ID('dbo')
            AND t.is_ms_shipped = 0
            AND i.object_id > 255
        GROUP BY 
            t.name, t.schema_id, p.rows
        ORDER BY 
            t.name
        """

        results = conn.execute_query(query)

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table_count": len(results),
            "tables": results
        }

    except Exception as e:
        logger.error(f"Failed to list tables: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_table_schema(server_name: str, database_name: str, table_name: str) -> Dict[str, Any]:
    """
    Get detailed schema information for a table.

    Args:
        server_name: SQL Server instance name
        database_name: Target database
        table_name: Table name (dbo schema)

    Returns:
        Dictionary with table schema details
    """
    try:
        conn = SQLServerConnection(server_name, database_name)

        query = """
        SELECT 
            c.name as column_name,
            t.name as data_type,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable,
            c.is_identity,
            ISNULL(i.is_primary_key, 0) as is_primary_key
        FROM 
            sys.columns c
        INNER JOIN 
            sys.types t ON c.user_type_id = t.user_type_id
        LEFT JOIN 
            sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        LEFT JOIN 
            sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id AND i.is_primary_key = 1
        WHERE 
            c.object_id = OBJECT_ID(?)
        ORDER BY 
            c.column_id
        """

        results = conn.execute_query(query, params=(f"dbo.{table_name}",))

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table": table_name,
            "columns": results
        }

    except Exception as e:
        logger.error(f"Failed to get table schema: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def query_table(
    server_name: str,
    database_name: str,
    table_name: str,
    columns: Optional[str] = None,
    where_clause: Optional[str] = None,
    top_n: int = 100
) -> Dict[str, Any]:
    """
    Execute a SELECT query on a dbo table.

    Args:
        server_name: SQL Server instance name
        database_name: Target database
        table_name: Table name (dbo schema)
        columns: Comma-separated column names (default: *)
        where_clause: WHERE condition (without WHERE keyword)
        top_n: Maximum number of rows to return

    Returns:
        Dictionary with query results
    """
    try:
        conn = SQLServerConnection(server_name, database_name)

        # Validate table exists
        validate_query = "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?"
        validation = conn.execute_query(validate_query, params=(table_name,))
        if not validation:
            return {
                "success": False,
                "error": f"Table 'dbo.{table_name}' does not exist"
            }

        # Build query
        columns_str = columns if columns else "*"
        query = f"SELECT TOP {top_n} {columns_str} FROM dbo.[{table_name}]"

        if where_clause:
            query += f" WHERE {where_clause}"

        results = conn.execute_query(query)

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table": table_name,
            "row_count": len(results),
            "rows": results
        }

    except Exception as e:
        logger.error(f"Failed to query table: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def update_table(
    server_name: str,
    database_name: str,
    table_name: str,
    set_clause: str,
    where_clause: str
) -> Dict[str, Any]:
    """
    Execute an UPDATE query on a dbo table (DEV environments only: DOA, DOB).

    Args:
        server_name: SQL Server instance name (must be DOA or DOB)
        database_name: Target database
        table_name: Table name (dbo schema)
        set_clause: SET clause (e.g., "column1 = 'value1', column2 = 123")
        where_clause: WHERE condition (without WHERE keyword) - REQUIRED

    Returns:
        Dictionary with operation results
    """
    try:
        # Check environment restriction
        if not is_dev_environment(server_name):
            return {
                "success": False,
                "error": f"UPDATE operations are only allowed on DEV environments (DOA, DOB). Server '{server_name}' is not a dev environment.",
                "server": server_name
            }

        # Require WHERE clause
        if not where_clause or where_clause.strip() == "":
            return {
                "success": False,
                "error": "WHERE clause is required for UPDATE operations to prevent accidental full table updates"
            }

        conn = SQLServerConnection(server_name, database_name)

        # Validate table exists
        validate_query = "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?"
        validation = conn.execute_query(validate_query, params=(table_name,))
        if not validation:
            return {
                "success": False,
                "error": f"Table 'dbo.{table_name}' does not exist"
            }

        # Build and execute UPDATE query
        query = f"UPDATE dbo.[{table_name}] SET {set_clause} WHERE {where_clause}"
        rows_affected = conn.execute_non_query(query)

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table": table_name,
            "rows_affected": rows_affected,
            "operation": "UPDATE"
        }

    except Exception as e:
        logger.error(f"Failed to update table: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def insert_into_table(
    server_name: str,
    database_name: str,
    table_name: str,
    columns: str,
    values: str
) -> Dict[str, Any]:
    """
    Execute an INSERT query on a dbo table (DEV environments only: DOA, DOB).

    Args:
        server_name: SQL Server instance name (must be DOA or DOB)
        database_name: Target database
        table_name: Table name (dbo schema)
        columns: Comma-separated column names
        values: Comma-separated values (must match columns)

    Returns:
        Dictionary with operation results
    """
    try:
        # Check environment restriction
        if not is_dev_environment(server_name):
            return {
                "success": False,
                "error": f"INSERT operations are only allowed on DEV environments (DOA, DOB). Server '{server_name}' is not a dev environment.",
                "server": server_name
            }

        conn = SQLServerConnection(server_name, database_name)

        # Validate table exists
        validate_query = "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?"
        validation = conn.execute_query(validate_query, params=(table_name,))
        if not validation:
            return {
                "success": False,
                "error": f"Table 'dbo.{table_name}' does not exist"
            }

        # Build and execute INSERT query
        query = f"INSERT INTO dbo.[{table_name}] ({columns}) VALUES ({values})"
        rows_affected = conn.execute_non_query(query)

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table": table_name,
            "rows_affected": rows_affected,
            "operation": "INSERT"
        }

    except Exception as e:
        logger.error(f"Failed to insert into table: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def delete_from_table(
    server_name: str,
    database_name: str,
    table_name: str,
    where_clause: str
) -> Dict[str, Any]:
    """
    Execute a DELETE query on a dbo table (DEV environments only: DOA, DOB).

    Args:
        server_name: SQL Server instance name (must be DOA or DOB)
        database_name: Target database
        table_name: Table name (dbo schema)
        where_clause: WHERE condition (without WHERE keyword) - REQUIRED

    Returns:
        Dictionary with operation results
    """
    try:
        # Check environment restriction
        if not is_dev_environment(server_name):
            return {
                "success": False,
                "error": f"DELETE operations are only allowed on DEV environments (DOA, DOB). Server '{server_name}' is not a dev environment.",
                "server": server_name
            }

        # Require WHERE clause
        if not where_clause or where_clause.strip() == "":
            return {
                "success": False,
                "error": "WHERE clause is required for DELETE operations to prevent accidental full table deletion"
            }

        conn = SQLServerConnection(server_name, database_name)

        # Validate table exists
        validate_query = "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?"
        validation = conn.execute_query(validate_query, params=(table_name,))
        if not validation:
            return {
                "success": False,
                "error": f"Table 'dbo.{table_name}' does not exist"
            }

        # Build and execute DELETE query
        query = f"DELETE FROM dbo.[{table_name}] WHERE {where_clause}"
        rows_affected = conn.execute_non_query(query)

        return {
            "success": True,
            "server": server_name,
            "database": database_name,
            "table": table_name,
            "rows_affected": rows_affected,
            "operation": "DELETE"
        }

    except Exception as e:
        logger.error(f"Failed to delete from table: {e}")
        return {
            "success": False,
            "error": str(e)
        }
