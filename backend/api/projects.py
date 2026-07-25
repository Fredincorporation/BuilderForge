"""Project Management Endpoints for BuilderForge.

Routes for creating, running multi-agent pipelines, retrieving status, reading logs, and exporting ZIP launch packages.
"""

from __future__ import annotations

import io
import json
import zipfile
import logging
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from utils.db import (
    db_save_project,
    db_get_all_projects,
    db_get_project_by_id,
    db_delete_project,
)
from agents.coordinator import CoordinatorAgent

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory log buffer & thread pool for async task execution
_logs_store: Dict[str, List[str]] = {}
_executor = ThreadPoolExecutor(max_workers=4)


def _run_pipeline_background(project_id: str, title: str, description: str, category: str):
    """Background task function to execute the 4-phase coordinator pipeline."""
    try:
        _logs_store[project_id] = [f"[{datetime.now().isoformat()}] Multi-agent pipeline queued for Project '{title}'"]
        
        def log_callback(msg: str, progress: float):
            formatted = f"[{datetime.now().isoformat()}] {msg}"
            if project_id not in _logs_store:
                _logs_store[project_id] = []
            _logs_store[project_id].append(formatted)
            
            # Update project progress in DB
            proj = db_get_project_by_id(project_id)
            if proj:
                proj["progress"] = progress
                proj["phase"] = "IN_PROGRESS" if progress < 1.0 else "COMPLETE"
                db_save_project(proj)

        coordinator = CoordinatorAgent(mode="SIMULATED")
        results = coordinator.execute_pipeline(
            project_id=project_id,
            project_title=title,
            description=description,
            category=category,
            log_callback=log_callback
        )
        
        # Save complete result to DB
        proj = db_get_project_by_id(project_id) or {}
        proj["opportunity_report"] = results["opportunity_report"]
        proj["launch_assets"] = results["launch_assets"]
        proj["deployment_plan"] = results["deployment_plan"]
        proj["metrics_report"] = results["metrics_report"]
        proj["phase"] = "COMPLETE"
        proj["progress"] = 1.0
        db_save_project(proj)
        
        _logs_store[project_id].append(f"[{datetime.now().isoformat()}] Pipeline execution finished successfully!")
        logger.info(f"Pipeline finished for project {project_id}")

    except Exception as e:
        logger.error(f"Error in background pipeline for {project_id}: {e}", exc_info=True)
        if project_id not in _logs_store:
            _logs_store[project_id] = []
        _logs_store[project_id].append(f"[{datetime.now().isoformat()}] ERROR: {str(e)}")
        
        proj = db_get_project_by_id(project_id) or {}
        proj["phase"] = "FAILED"
        db_save_project(proj)


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(request: dict) -> dict:
    """Create a new project persisted in SQLite."""
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
            "created_at": datetime.now().isoformat(),
        }
        
        saved = db_save_project(project)
        _logs_store[project_id] = [f"[{datetime.now().isoformat()}] Project created: {title}"]
        logger.info(f"Created project: {project_id} - {title}")
        
        return {
            "status": "success",
            "project": saved
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/projects/{project_id}/run")
async def run_project_pipeline(project_id: str, request: Optional[dict] = None) -> dict:
    """Start the multi-agent pipeline (Researcher -> Creator -> Executor -> Analyzer)."""
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        # Launch background thread
        _executor.submit(
            _run_pipeline_background,
            project_id=project_id,
            title=project.get("title", ""),
            description=project.get("description", ""),
            category=project.get("category", "General")
        )
        
        return {
            "status": "accepted",
            "project_id": project_id,
            "message": f"Multi-agent pipeline started for project {project_id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting pipeline for {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/projects")
async def list_projects() -> dict:
    """List all stored projects from SQLite."""
    try:
        projects = db_get_all_projects()
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
    """Get a specific project by ID with full results & logs."""
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        # Attach logs if available
        project["logs"] = _logs_store.get(project_id, [])
        
        return {
            "status": "success",
            "project": project
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/projects/{project_id}/logs")
async def get_project_logs(project_id: str) -> dict:
    """Get live agent logs for a running project."""
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        logs = _logs_store.get(project_id, [])
        return {
            "status": "success",
            "project_id": project_id,
            "progress": project.get("progress", 0.0),
            "phase": project.get("phase", "IDEA_INPUT"),
            "log_count": len(logs),
            "logs": logs
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching logs for {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch("/projects/{project_id}")
async def update_project(project_id: str, request: dict) -> dict:
    """Update project fields."""
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        if "title" in request:
            project["title"] = request["title"]
        if "description" in request:
            project["description"] = request["description"]
        if "phase" in request:
            project["phase"] = request["phase"]
        if "progress" in request:
            project["progress"] = min(1.0, max(0.0, float(request["progress"])))
        
        saved = db_save_project(project)
        return {
            "status": "success",
            "project": saved
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
async def delete_project_endpoint(project_id: str) -> dict:
    """Delete a project by ID."""
    try:
        deleted = db_delete_project(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
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


@router.get("/projects/{project_id}/export")
async def export_project(project_id: str):
    """
    Generate a downloadable ZIP package containing all project artifacts:
    - contract.sol
    - tokenomics.json
    - pitch_deck.md
    - asp_manifest.json
    - README.md
    """
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # README.md
            readme_content = f"""# {project.get('title', 'BuilderForge Project')}
{project.get('description', '')}

Category: {project.get('category', 'General')}
Phase: {project.get('phase', 'COMPLETE')}
Generated by BuilderForge OKX Agentic Service Provider (ASP).
"""
            zip_file.writestr("README.md", readme_content)

            # Contract code
            assets = project.get("launch_assets") or {}
            contract_code = assets.get("smart_contract_code") if isinstance(assets, dict) else """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract BuilderForgeToken { string public name = "BuilderForge Token"; }"""
            zip_file.writestr("contract.sol", contract_code)

            # Tokenomics
            tokenomics_data = {
                "token_name": assets.get("token_name", project.get("title")),
                "token_symbol": assets.get("token_symbol", "BFT"),
                "total_supply": assets.get("total_supply", "100,000,000"),
                "allocations": assets.get("allocations", {"Community": "50%", "Team": "20%", "Ecosystem": "30%"})
            }
            zip_file.writestr("tokenomics.json", json.dumps(tokenomics_data, indent=2))

            # Pitch Deck
            pitch_text = f"""# Pitch Deck: {project.get('title')}

## Elevator Pitch
{assets.get('elevator_pitch', 'Autonomous Web3 application launched with BuilderForge on OKX.')}

## Key Features
- Multi-Agent Pipeline Execution
- Native OKX Wallet & X Layer Testnet Deployment
- Listed Agentic Service Provider (ASP) Manifest

## Marketing Hooks
""" + "\n".join([f"- {hook}" for hook in assets.get('marketing_hooks', [])])

            zip_file.writestr("pitch_deck.md", pitch_text)

            # ASP Manifest
            metrics = project.get("metrics_report") or {}
            manifest_data = metrics.get("asp_manifest") or {
                "schema_version": "1.0.0",
                "service_id": f"asp.{project_id}.okx",
                "title": project.get("title"),
                "description": project.get("description"),
            }
            zip_file.writestr("asp_manifest.json", json.dumps(manifest_data, indent=2))

        zip_buffer.seek(0)
        filename = f"builderforge_{project_id}.zip"
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
