"""Project Management Endpoints.

Routes for creating, retrieving, and managing projects.
"""

from __future__ import annotations

import logging
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

try:
    from utils.models import ProjectData
    from utils.state import save_project, get_current_project
except ImportError:
    ProjectData = None
    save_project = None
    get_current_project = None

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory project storage (replace with database in production)
_projects_db: dict[str, dict] = {}


# ============================================================================
# Models
# ============================================================================
class ProjectCreateRequest:
    """Request body for creating a project."""
    def __init__(self, title: str, description: str, category: Optional[str] = None):
        self.title = title
        self.description = description
        self.category = category or "General"


class ProjectResponse:
    """Response model for project."""
    def __init__(self, id: str, title: str, description: str, phase: str, progress: float):
        self.id = id
        self.title = title
        self.description = description
        self.phase = phase
        self.progress = progress


# ============================================================================
# Endpoints
# ============================================================================
@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(request: dict) -> dict:
    """
    Create a new project.
    
    Request body:
    - title: str (required)
    - description: str (required)
    - category: str (optional, default: "General")
    
    Returns: Project object with id, title, description, phase, progress
    """
    try:
        title = request.get("title", "").strip()
        description = request.get("description", "").strip()
        category = request.get("category", "General").strip()
        
        if not title or not description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="title and description are required"
            )
        
        project_id = str(uuid4())[:8]
        project = {
            "id": project_id,
            "title": title,
            "description": description,
            "category": category,
            "phase": "IDEA_INPUT",
            "progress": 0.0,
            "created_at": None,  # Will be set by utils.models.ProjectData if used
        }
        
        _projects_db[project_id] = project
        logger.info(f"Created project: {project_id} - {title}")
        
        return {
            "status": "success",
            "project": project
        }
    
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/projects")
async def list_projects() -> dict:
    """
    List all projects.
    
    Returns: List of project objects
    """
    try:
        projects = list(_projects_db.values())
        return {
            "status": "success",
            "count": len(projects),
            "projects": projects
        }
    
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> dict:
    """
    Get a specific project by ID.
    
    Path parameters:
    - project_id: str (UUID)
    
    Returns: Project object
    """
    try:
        if project_id not in _projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        return {
            "status": "success",
            "project": _projects_db[project_id]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch("/projects/{project_id}")
async def update_project(project_id: str, request: dict) -> dict:
    """
    Update a project.
    
    Path parameters:
    - project_id: str (UUID)
    
    Request body (all optional):
    - title: str
    - description: str
    - phase: str
    - progress: float
    
    Returns: Updated project object
    """
    try:
        if project_id not in _projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        project = _projects_db[project_id]
        
        # Update only provided fields
        if "title" in request:
            project["title"] = request["title"]
        if "description" in request:
            project["description"] = request["description"]
        if "phase" in request:
            project["phase"] = request["phase"]
        if "progress" in request:
            project["progress"] = min(1.0, max(0.0, float(request["progress"])))
        
        logger.info(f"Updated project: {project_id}")
        
        return {
            "status": "success",
            "project": project
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str) -> dict:
    """
    Delete a project.
    
    Path parameters:
    - project_id: str (UUID)
    
    Returns: Success message
    """
    try:
        if project_id not in _projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        del _projects_db[project_id]
        logger.info(f"Deleted project: {project_id}")
        
        return {
            "status": "success",
            "message": f"Project {project_id} deleted"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
