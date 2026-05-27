"""
Tools for managing SQL Server instances and services.
"""
from typing import Any, Dict
import logging
import win32serviceutil
import win32service
import time
from ..connection import SQLServerConnection

logger = logging.getLogger(__name__)


def get_instance_status(server_name: str) -> Dict[str, Any]:
    """
    Get SQL Server instance status and information.

    Args:
        server_name: SQL Server instance name

    Returns:
        Dictionary with instance status and metadata
    """
    try:
        conn = SQLServerConnection(server_name, "master")

        query = """
        SELECT 
            @@VERSION as version,
            @@SERVERNAME as server_name,
            SERVERPROPERTY('ProductVersion') as product_version,
            SERVERPROPERTY('ProductLevel') as product_level,
            SERVERPROPERTY('Edition') as edition,
            SERVERPROPERTY('IsClustered') as is_clustered,
            SERVERPROPERTY('IsHadrEnabled') as is_hadr_enabled,
            CREATE_DATE as sql_server_start_time
        FROM 
            sys.databases 
        WHERE 
            name = 'tempdb'
        """

        results = conn.execute_query(query, fetch_all=False)

        # Get database count
        db_query = "SELECT COUNT(*) as db_count FROM sys.databases WHERE state = 0"
        db_count = conn.execute_query(db_query, fetch_all=False)

        # Get connection count
        conn_query = "SELECT COUNT(*) as connection_count FROM sys.dm_exec_sessions WHERE is_user_process = 1"
        conn_count = conn.execute_query(conn_query, fetch_all=False)

        return {
            "success": True,
            "server": server_name,
            "status": "Online",
            "instance_info": results[0] if results else {},
            "database_count": db_count[0]['db_count'] if db_count else 0,
            "user_connections": conn_count[0]['connection_count'] if conn_count else 0
        }

    except Exception as e:
        logger.error(f"Failed to get instance status: {e}")
        return {
            "success": False,
            "server": server_name,
            "status": "Offline or Inaccessible",
            "error": str(e)
        }


def get_service_name(server_name: str, service_type: str = "engine") -> str:
    """
    Get Windows service name for SQL Server instance.

    Args:
        server_name: SQL Server instance name
        service_type: 'engine' or 'agent'

    Returns:
        Windows service name
    """
    # Parse instance name
    if '\\' in server_name:
        instance = server_name.split('\\')[1]
    else:
        instance = None

    if service_type == "engine":
        return "MSSQLSERVER" if not instance else f"MSSQL${instance}"
    elif service_type == "agent":
        return "SQLSERVERAGENT" if not instance else f"SQLAgent${instance}"
    else:
        raise ValueError(f"Invalid service_type: {service_type}")


def restart_sql_service(
    server_name: str,
    service_name: str = None,
    force: bool = False
) -> Dict[str, Any]:
    """
    Restart SQL Server service (requires admin privileges).

    Args:
        server_name: SQL Server instance name
        service_name: Windows service name (auto-detected if not provided)
        force: Force restart without graceful shutdown

    Returns:
        Dictionary with restart operation results
    """
    try:
        # Auto-detect service name if not provided
        if not service_name:
            service_name = get_service_name(server_name, "engine")

        logger.info(f"Attempting to restart service: {service_name}")

        # Check if service exists
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)
        except Exception as e:
            return {
                "success": False,
                "error": f"Service '{service_name}' not found: {str(e)}"
            }

        # Stop service
        logger.info(f"Stopping service: {service_name}")
        if force:
            win32serviceutil.StopService(service_name)
        else:
            win32serviceutil.StopServiceWithDeps(service_name)

        # Wait for service to stop
        timeout = 60  # seconds
        elapsed = 0
        while elapsed < timeout:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status == win32service.SERVICE_STOPPED:
                break
            time.sleep(2)
            elapsed += 2

        if status != win32service.SERVICE_STOPPED:
            return {
                "success": False,
                "error": f"Service did not stop within {timeout} seconds"
            }

        logger.info(f"Service stopped: {service_name}")

        # Start service
        logger.info(f"Starting service: {service_name}")
        win32serviceutil.StartService(service_name)

        # Wait for service to start
        elapsed = 0
        while elapsed < timeout:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status == win32service.SERVICE_RUNNING:
                break
            time.sleep(2)
            elapsed += 2

        if status != win32service.SERVICE_RUNNING:
            return {
                "success": False,
                "error": f"Service did not start within {timeout} seconds"
            }

        logger.info(f"Service started: {service_name}")

        return {
            "success": True,
            "server": server_name,
            "service_name": service_name,
            "operation": "restart",
            "message": f"Service '{service_name}' restarted successfully"
        }

    except Exception as e:
        logger.error(f"Failed to restart service: {e}")
        return {
            "success": False,
            "error": str(e),
            "note": "Ensure the application is running with administrator privileges"
        }


def restart_agent_service(
    server_name: str,
    service_name: str = None
) -> Dict[str, Any]:
    """
    Restart SQL Server Agent service (requires admin privileges).

    Args:
        server_name: SQL Server instance name
        service_name: Windows service name (auto-detected if not provided)

    Returns:
        Dictionary with restart operation results
    """
    try:
        # Auto-detect service name if not provided
        if not service_name:
            service_name = get_service_name(server_name, "agent")

        logger.info(f"Attempting to restart Agent service: {service_name}")

        # Check if service exists
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)
        except Exception as e:
            return {
                "success": False,
                "error": f"Service '{service_name}' not found: {str(e)}"
            }

        # Restart service
        win32serviceutil.RestartService(service_name)

        # Wait for service to restart
        timeout = 30  # seconds
        elapsed = 0
        while elapsed < timeout:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            if status == win32service.SERVICE_RUNNING:
                break
            time.sleep(2)
            elapsed += 2

        if status != win32service.SERVICE_RUNNING:
            return {
                "success": False,
                "error": f"Service did not restart within {timeout} seconds"
            }

        logger.info(f"Agent service restarted: {service_name}")

        return {
            "success": True,
            "server": server_name,
            "service_name": service_name,
            "operation": "restart",
            "message": f"Agent service '{service_name}' restarted successfully"
        }

    except Exception as e:
        logger.error(f"Failed to restart Agent service: {e}")
        return {
            "success": False,
            "error": str(e),
            "note": "Ensure the application is running with administrator privileges"
        }


def get_service_status(server_name: str, service_type: str = "engine") -> Dict[str, Any]:
    """
    Get Windows service status for SQL Server.

    Args:
        server_name: SQL Server instance name
        service_type: 'engine' or 'agent'

    Returns:
        Dictionary with service status
    """
    try:
        service_name = get_service_name(server_name, service_type)

        status_code = win32serviceutil.QueryServiceStatus(service_name)[1]

        status_map = {
            win32service.SERVICE_STOPPED: "Stopped",
            win32service.SERVICE_START_PENDING: "Starting",
            win32service.SERVICE_STOP_PENDING: "Stopping",
            win32service.SERVICE_RUNNING: "Running",
            win32service.SERVICE_CONTINUE_PENDING: "Continuing",
            win32service.SERVICE_PAUSE_PENDING: "Pausing",
            win32service.SERVICE_PAUSED: "Paused"
        }

        status = status_map.get(status_code, "Unknown")

        return {
            "success": True,
            "server": server_name,
            "service_name": service_name,
            "service_type": service_type,
            "status": status,
            "status_code": status_code
        }

    except Exception as e:
        logger.error(f"Failed to get service status: {e}")
        return {
            "success": False,
            "error": str(e)
        }
