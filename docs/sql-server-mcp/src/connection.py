"""
SQL Server connection management with Windows Authentication.
"""
import pyodbc
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class SQLServerConnection:
    """Manages SQL Server connections using Windows Authentication."""

    def __init__(self, server_name: str, database: str = "master", timeout: int = 30):
        """
        Initialize SQL Server connection.

        Args:
            server_name: SQL Server instance name (e.g., 'localhost', 'SERVER\\INSTANCE')
            database: Target database (default: 'master')
            timeout: Connection timeout in seconds (default: 30)
        """
        self.server_name = server_name
        self.database = database
        self.timeout = timeout
        self.connection_string = self._build_connection_string()

    def _build_connection_string(self) -> str:
        """Build connection string with Windows Authentication."""
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server_name};"
            f"DATABASE={self.database};"
            f"Trusted_Connection=yes;"
            f"Connection Timeout={self.timeout};"
        )

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.

        Yields:
            pyodbc.Connection: Active database connection

        Raises:
            pyodbc.Error: If connection fails
        """
        conn = None
        try:
            logger.info(f"Connecting to {self.server_name}/{self.database}")
            conn = pyodbc.connect(self.connection_string)
            yield conn
        except pyodbc.Error as e:
            logger.error(f"Connection failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.info(f"Connection closed to {self.server_name}/{self.database}")

    def execute_query(
        self, query: str, params: Optional[tuple] = None, fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.

        Args:
            query: SQL query to execute
            params: Optional query parameters
            fetch_all: If True, fetch all results; otherwise fetch one

        Returns:
            List of dictionaries with column names as keys

        Raises:
            pyodbc.Error: If query execution fails
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Get column names
                columns = [column[0] for column in cursor.description] if cursor.description else []

                # Fetch results
                if fetch_all:
                    rows = cursor.fetchall()
                else:
                    row = cursor.fetchone()
                    rows = [row] if row else []

                # Convert to list of dictionaries
                results = []
                for row in rows:
                    results.append(dict(zip(columns, row)))

                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results

            except pyodbc.Error as e:
                logger.error(f"Query execution failed: {e}")
                raise
            finally:
                cursor.close()

    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query to execute
            params: Optional query parameters

        Returns:
            Number of rows affected

        Raises:
            pyodbc.Error: If query execution fails
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                conn.commit()
                rows_affected = cursor.rowcount

                logger.info(f"Non-query executed successfully, {rows_affected} rows affected")
                return rows_affected

            except pyodbc.Error as e:
                conn.rollback()
                logger.error(f"Non-query execution failed: {e}")
                raise
            finally:
                cursor.close()

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection and return server information.

        Returns:
            Dictionary with server version and connection status
        """
        try:
            query = """
            SELECT 
                @@VERSION as version,
                @@SERVERNAME as server_name,
                DB_NAME() as database_name,
                SUSER_SNAME() as current_user
            """
            result = self.execute_query(query, fetch_all=False)
            if result:
                return {
                    "status": "connected",
                    "server_info": result[0]
                }
            return {"status": "failed", "error": "No result returned"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


def get_environment_from_server(server_name: str) -> str:
    """
    Determine environment from server name.

    Args:
        server_name: SQL Server instance name

    Returns:
        Environment name: 'DOA', 'DOB', 'PRODUCTION', 'UNKNOWN'
    """
    server_upper = server_name.upper()

    if "DOA" in server_upper:
        return "DOA"
    elif "DOB" in server_upper:
        return "DOB"
    elif any(prod in server_upper for prod in ["PROD", "PRD", "PRODUCTION"]):
        return "PRODUCTION"
    else:
        return "UNKNOWN"


def is_dev_environment(server_name: str) -> bool:
    """
    Check if server is in a dev environment (DOA or DOB).

    Args:
        server_name: SQL Server instance name

    Returns:
        True if dev environment, False otherwise
    """
    env = get_environment_from_server(server_name)
    return env in ["DOA", "DOB"]
