"""
Tools for managing SQL Server Agent jobs.
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import logging
from ..connection import SQLServerConnection

logger = logging.getLogger(__name__)


def list_agent_jobs(server_name: str, enabled_only: bool = False) -> Dict[str, Any]:
    """
    List all SQL Server Agent jobs.

    Args:
        server_name: SQL Server instance name
        enabled_only: If True, only return enabled jobs

    Returns:
        Dictionary with list of jobs
    """
    try:
        conn = SQLServerConnection(server_name, "msdb")

        query = """
        SELECT 
            j.job_id,
            j.name as job_name,
            j.enabled,
            j.description,
            SUSER_SNAME(j.owner_sid) as owner,
            j.date_created,
            j.date_modified,
            CASE 
                WHEN ja.run_requested_date IS NOT NULL AND ja.stop_execution_date IS NULL THEN 'Running'
                ELSE 'Idle'
            END as current_status
        FROM 
            msdb.dbo.sysjobs j
        LEFT JOIN 
            msdb.dbo.sysjobactivity ja ON j.job_id = ja.job_id
            AND ja.session_id = (SELECT MAX(session_id) FROM msdb.dbo.sysjobactivity)
        WHERE 
            1=1
            {enabled_filter}
        ORDER BY 
            j.name
        """

        enabled_filter = "AND j.enabled = 1" if enabled_only else ""
        query = query.format(enabled_filter=enabled_filter)

        results = conn.execute_query(query)

        return {
            "success": True,
            "server": server_name,
            "job_count": len(results),
            "jobs": results
        }

    except Exception as e:
        logger.error(f"Failed to list agent jobs: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_job_history(
    server_name: str,
    job_name: Optional[str] = None,
    last_n_runs: int = 10,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get execution history for SQL Server Agent jobs.

    Args:
        server_name: SQL Server instance name
        job_name: Specific job name (if None, returns all jobs)
        last_n_runs: Number of recent runs per job
        date_from: Start date filter (YYYY-MM-DD)
        date_to: End date filter (YYYY-MM-DD)

    Returns:
        Dictionary with job execution history
    """
    try:
        conn = SQLServerConnection(server_name, "msdb")

        # Build date filters
        date_filter = ""
        if date_from:
            date_filter += f" AND h.run_date >= CAST(REPLACE('{date_from}', '-', '') AS INT)"
        if date_to:
            date_filter += f" AND h.run_date <= CAST(REPLACE('{date_to}', '-', '') AS INT)"

        job_filter = ""
        if job_name:
            job_filter = "AND j.name = ?"

        query = f"""
        SELECT TOP {last_n_runs * 10}
            j.name as job_name,
            h.step_id,
            h.step_name,
            h.run_date,
            h.run_time,
            CASE h.run_status
                WHEN 0 THEN 'Failed'
                WHEN 1 THEN 'Succeeded'
                WHEN 2 THEN 'Retry'
                WHEN 3 THEN 'Canceled'
                WHEN 4 THEN 'In Progress'
            END as run_status,
            h.run_duration,
            h.message,
            h.retries_attempted,
            CAST(
                CAST(h.run_date AS VARCHAR(8)) + ' ' +
                STUFF(STUFF(RIGHT('000000' + CAST(h.run_time AS VARCHAR(6)), 6), 5, 0, ':'), 3, 0, ':')
                AS DATETIME
            ) as run_datetime
        FROM 
            msdb.dbo.sysjobs j
        INNER JOIN 
            msdb.dbo.sysjobhistory h ON j.job_id = h.job_id
        WHERE 
            h.step_id = 0  -- 0 indicates job outcome
            {job_filter}
            {date_filter}
        ORDER BY 
            h.run_date DESC, h.run_time DESC
        """

        if job_name:
            results = conn.execute_query(query, params=(job_name,))
        else:
            results = conn.execute_query(query)

        # Limit to last_n_runs per job if no specific job requested
        if not job_name:
            job_runs = {}
            filtered_results = []
            for result in results:
                job = result['job_name']
                if job not in job_runs:
                    job_runs[job] = 0
                if job_runs[job] < last_n_runs:
                    filtered_results.append(result)
                    job_runs[job] += 1
            results = filtered_results

        return {
            "success": True,
            "server": server_name,
            "job_name": job_name if job_name else "All jobs",
            "history_count": len(results),
            "history": results
        }

    except Exception as e:
        logger.error(f"Failed to get job history: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_job_status(server_name: str, job_name: str) -> Dict[str, Any]:
    """
    Get current status of a specific SQL Server Agent job.

    Args:
        server_name: SQL Server instance name
        job_name: Job name

    Returns:
        Dictionary with current job status
    """
    try:
        conn = SQLServerConnection(server_name, "msdb")

        query = """
        SELECT 
            j.name as job_name,
            j.enabled,
            j.description,
            CASE 
                WHEN ja.run_requested_date IS NOT NULL AND ja.stop_execution_date IS NULL THEN 'Running'
                WHEN ja.stop_execution_date IS NOT NULL THEN 'Stopped'
                ELSE 'Idle'
            END as current_status,
            ja.start_execution_date,
            ja.last_executed_step_id,
            ja.last_executed_step_date,
            js.next_run_date,
            js.next_run_time,
            CASE 
                WHEN js.next_run_date > 0 THEN
                    CAST(
                        CAST(js.next_run_date AS VARCHAR(8)) + ' ' +
                        STUFF(STUFF(RIGHT('000000' + CAST(js.next_run_time AS VARCHAR(6)), 6), 5, 0, ':'), 3, 0, ':')
                        AS DATETIME
                    )
                ELSE NULL
            END as next_scheduled_run,
            h.run_date as last_run_date,
            h.run_time as last_run_time,
            CASE h.run_status
                WHEN 0 THEN 'Failed'
                WHEN 1 THEN 'Succeeded'
                WHEN 2 THEN 'Retry'
                WHEN 3 THEN 'Canceled'
                WHEN 4 THEN 'In Progress'
            END as last_run_status,
            h.run_duration as last_run_duration
        FROM 
            msdb.dbo.sysjobs j
        LEFT JOIN 
            msdb.dbo.sysjobactivity ja ON j.job_id = ja.job_id
            AND ja.session_id = (SELECT MAX(session_id) FROM msdb.dbo.sysjobactivity)
        LEFT JOIN 
            msdb.dbo.sysjobschedules js ON j.job_id = js.job_id
        LEFT JOIN 
            (SELECT job_id, MAX(instance_id) as max_instance_id 
             FROM msdb.dbo.sysjobhistory 
             WHERE step_id = 0 
             GROUP BY job_id) h_max ON j.job_id = h_max.job_id
        LEFT JOIN 
            msdb.dbo.sysjobhistory h ON h_max.job_id = h.job_id 
            AND h_max.max_instance_id = h.instance_id
        WHERE 
            j.name = ?
        """

        results = conn.execute_query(query, params=(job_name,))

        if not results:
            return {
                "success": False,
                "error": f"Job '{job_name}' not found"
            }

        return {
            "success": True,
            "server": server_name,
            "job_status": results[0]
        }

    except Exception as e:
        logger.error(f"Failed to get job status: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def get_failed_jobs(server_name: str, hours: int = 24) -> Dict[str, Any]:
    """
    Get jobs that failed in the last N hours.

    Args:
        server_name: SQL Server instance name
        hours: Look back period in hours

    Returns:
        Dictionary with failed jobs
    """
    try:
        conn = SQLServerConnection(server_name, "msdb")

        # Calculate date threshold
        threshold_date = datetime.now() - timedelta(hours=hours)
        threshold_date_int = int(threshold_date.strftime("%Y%m%d"))

        query = """
        SELECT 
            j.name as job_name,
            h.step_id,
            h.step_name,
            h.run_date,
            h.run_time,
            h.run_duration,
            h.message,
            CAST(
                CAST(h.run_date AS VARCHAR(8)) + ' ' +
                STUFF(STUFF(RIGHT('000000' + CAST(h.run_time AS VARCHAR(6)), 6), 5, 0, ':'), 3, 0, ':')
                AS DATETIME
            ) as run_datetime
        FROM 
            msdb.dbo.sysjobs j
        INNER JOIN 
            msdb.dbo.sysjobhistory h ON j.job_id = h.job_id
        WHERE 
            h.run_status = 0  -- Failed
            AND h.step_id = 0  -- Job outcome
            AND h.run_date >= ?
        ORDER BY 
            h.run_date DESC, h.run_time DESC
        """

        results = conn.execute_query(query, params=(threshold_date_int,))

        return {
            "success": True,
            "server": server_name,
            "lookback_hours": hours,
            "failed_job_count": len(results),
            "failed_jobs": results
        }

    except Exception as e:
        logger.error(f"Failed to get failed jobs: {e}")
        return {
            "success": False,
            "error": str(e)
        }
