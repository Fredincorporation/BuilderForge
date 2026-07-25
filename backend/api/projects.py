"""Project Management Endpoints.

Routes for creating, retrieving, updating, deleting, and exporting projects.
Backed by persistent SQLite storage (utils/db.py).
"""

from __future__ import annotations

import io
import json
import zipfile
import logging
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from utils.db import (
    db_save_project,
    db_get_all_projects,
    db_get_project_by_id,
    db_delete_project,
)

logger = logging.getLogger(__name__)
router = APIRouter()


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
        logger.info(f"Created project: {project_id} - {title}")
        
        return {
            "status": "success",
            "project": saved
        }
    
    except Exception as e:
        logger.error(f"Error creating project: {e}")
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
    """Get a specific project by ID."""
    try:
        project = db_get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
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
        logger.info(f"Updated project: {project_id}")
        
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
            contract_data = assets.get("smart_contract") if isinstance(assets, dict) else {}
            contract_code = contract_data.get("code") if isinstance(contract_data, dict) else """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BuilderForgeToken {
    string public name = "BuilderForge Token";
    string public symbol = "BFT";
    uint8 public decimals = 18;
    uint256 public totalSupply = 1000000 * 10**18;
}"""
            zip_file.writestr("contract.sol", contract_code)

            # Tokenomics
            tokenomics_data = assets.get("tokenomics") if isinstance(assets, dict) else {
                "name": project.get("title"),
                "total_supply": "100,000,000",
                "allocations": {"Community": "50%", "Team": "20%", "Ecosystem": "30%"}
            }
            zip_file.writestr("tokenomics.json", json.dumps(tokenomics_data, indent=2))

            # Pitch Deck
            pitch_data = assets.get("pitch_deck") if isinstance(assets, dict) else {
                "problem": "Web3 launch complexity",
                "solution": "Autonomous BuilderForge AI Crew execution"
            }
            zip_file.writestr("pitch_deck.md", f"# Pitch Deck\n\n```json\n{json.dumps(pitch_data, indent=2)}\n```")

            # ASP Manifest
            manifest_data = {
                "manifest_version": "1.0.0",
                "service_id": f"asp.{project_id}.okx",
                "title": project.get("title"),
                "description": project.get("description"),
                "agents": ["Coordinator", "Researcher", "Creator", "Executor", "Analyzer"],
                "pricing": {"model": "PAY_PER_JOB", "price_okt": "0.05"},
                "network": "OKC Testnet / OKX Chain"
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
