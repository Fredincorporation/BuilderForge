"""Crew Execution Endpoints.

Routes for running CrewAI workflows and tracking execution status.
"""

from __future__ import annotations

import logging
import asyncio
import json
from typing import Optional
from uuid import uuid4
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory task tracking (replace with database in production)
_tasks_db: dict[str, dict] = {}
_executor = ThreadPoolExecutor(max_workers=4)


# ============================================================================
# Helper: Import CrewAI (with fallback)
# ============================================================================
def _run_crew_workflow(project_id: str, phase: str, task_id: str):
    """
    Execute CrewAI workflow in a thread.
    Imports crew functions dynamically to avoid circular imports.
    """
    try:
        from crew.builderforge_crew import build_phase_crew
        from utils.models import ProjectData
        from utils.state import add_crew_log
        
        # Create mock project
        project = ProjectData(id=project_id, title=f"Project {project_id[:4]}")
        
        # Update task status
        _tasks_db[task_id]["status"] = "running"
        _tasks_db[task_id]["progress"] = 10
        _tasks_db[task_id]["logs"].append(f"[{datetime.now().isoformat()}] Building {phase} crew...")
        
        # Build and run crew
        crew = build_phase_crew(phase, verbose=True)
        
        _tasks_db[task_id]["progress"] = 30
        _tasks_db[task_id]["logs"].append(f"[{datetime.now().isoformat()}] Starting {phase} phase execution...")
        
        # Execute
        result = crew.kickoff(inputs={"project": project})
        
        _tasks_db[task_id]["progress"] = 90
        _tasks_db[task_id]["logs"].append(f"[{datetime.now().isoformat()}] Crew execution completed successfully!")
        
        # Store result
        _tasks_db[task_id]["result"] = {
            "phase": phase,
            "output": str(result),
            "status": "success",
        }
        _tasks_db[task_id]["status"] = "completed"
        _tasks_db[task_id]["progress"] = 100
        
    except Exception as e:
        logger.error(f"Error in crew execution {task_id}: {e}", exc_info=True)
        _tasks_db[task_id]["status"] = "error"
        _tasks_db[task_id]["logs"].append(f"[{datetime.now().isoformat()}] ERROR: {str(e)}")
        _tasks_db[task_id]["result"] = {
            "error": str(e),
            "status": "failed",
        }


# ============================================================================
# Models
# ============================================================================
class CrewRunRequest:
    """Request body for running crew."""
    def __init__(self, project_id: str, phase: Optional[str] = None):
        self.project_id = project_id
        self.phase = phase or "RESEARCH"


# ============================================================================
# Endpoints
# ============================================================================
@router.post("/crew/run", status_code=status.HTTP_202_ACCEPTED)
async def run_crew(request: dict) -> dict:
    """
    Start a crew execution workflow.
    
    Request body:
    - project_id: str (required)
    - phase: str (optional, default: "RESEARCH")
    
    Returns: Task ID for polling status
    """
    try:
        project_id = request.get("project_id", "").strip()
        phase = request.get("phase", "RESEARCH").strip().upper()
        
        if not project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="project_id is required"
            )
        
        valid_phases = ["RESEARCH", "CREATION", "EXECUTION", "ANALYSIS"]
        if phase not in valid_phases:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"phase must be one of: {', '.join(valid_phases)}"
            )
        
        task_id = str(uuid4())
        _tasks_db[task_id] = {
            "task_id": task_id,
            "project_id": project_id,
            "phase": phase,
            "status": "queued",
            "progress": 0,
            "logs": [f"[{datetime.now().isoformat()}] Task created for {phase} phase"],
            "result": None,
            "created_at": datetime.now().isoformat(),
        }
        
        logger.info(f"Started crew execution: task_id={task_id}, project_id={project_id}, phase={phase}")
        
        # Run crew in background thread
        _executor.submit(_run_crew_workflow, project_id, phase, task_id)
        
        return {
            "status": "accepted",
            "task_id": task_id,
            "message": f"Crew execution started for phase: {phase}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running crew: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/crew/{task_id}")
async def get_crew_status(task_id: str) -> dict:
    """
    Get crew execution status and logs.
    
    Path parameters:
    - task_id: str (UUID)
    
    Returns: Task status, progress, and logs
    """
    try:
        if task_id not in _tasks_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        task = _tasks_db[task_id]
        
        return {
            "status": "success",
            "task": {
                "task_id": task["task_id"],
                "project_id": task["project_id"],
                "phase": task["phase"],
                "status": task["status"],
                "progress": task["progress"],
                "log_count": len(task["logs"]),
                "created_at": task["created_at"],
            },
            "result": task["result"] if task["status"] == "completed" else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/crew/{task_id}/logs")
async def get_crew_logs(task_id: str, limit: Optional[int] = None) -> dict:
    """
    Get crew execution logs.
    
    Path parameters:
    - task_id: str (UUID)
    
    Query parameters:
    - limit: int (optional, default: all)
    
    Returns: Array of log entries
    """
    try:
        if task_id not in _tasks_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        task = _tasks_db[task_id]
        logs = task["logs"]
        
        if limit:
            logs = logs[-limit:]
        
        return {
            "status": "success",
            "task_id": task_id,
            "log_count": len(logs),
            "logs": logs
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching logs for {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/crew/{task_id}/cancel")
async def cancel_crew(task_id: str) -> dict:
    """
    Cancel a running crew execution.
    
    Path parameters:
    - task_id: str (UUID)
    
    Returns: Success message
    """
    try:
        if task_id not in _tasks_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        task = _tasks_db[task_id]
        
        if task["status"] == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel a completed task"
            )
        
        task["status"] = "cancelled"
        task["logs"].append(f"[{datetime.now().isoformat()}] Task cancelled by user")
        
        logger.info(f"Cancelled crew execution: {task_id}")
        
        return {
            "status": "success",
            "message": f"Task {task_id} cancelled"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
