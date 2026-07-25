"""SQLite Production Database Manager for BuilderForge.

Thread-safe SQLite persistence for projects, crew execution logs, and wallet state.
Data is persisted to data/builderforge.db.
"""

from __future__ import annotations

import os
import json
import sqlite3
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "builderforge.db")


def get_connection() -> sqlite3.Connection:
    """Get a thread-safe connection to the SQLite database."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables if they do not exist."""
    conn = get_connection()
    try:
        with conn:
            # Projects Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT DEFAULT 'General',
                    phase TEXT DEFAULT 'IDEA_INPUT',
                    progress REAL DEFAULT 0.0,
                    created_at TEXT,
                    opportunity_report TEXT,
                    launch_assets TEXT,
                    deployment_plan TEXT,
                    metrics_report TEXT
                )
            """)

            # Tasks Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crew_tasks (
                    task_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    phase TEXT DEFAULT 'RESEARCH',
                    status TEXT DEFAULT 'pending',
                    progress REAL DEFAULT 0.0,
                    logs TEXT,
                    result TEXT,
                    created_at TEXT
                )
            """)

            # Wallet Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wallet (
                    id TEXT PRIMARY KEY,
                    address TEXT NOT NULL,
                    chain TEXT DEFAULT 'okc',
                    connected INTEGER DEFAULT 1,
                    balance REAL DEFAULT 0.0,
                    connected_at TEXT
                )
            """)
        logger.info(f"Database initialized cleanly at {DB_PATH}")
    finally:
        conn.close()


# Ensure DB is initialized on module load
init_db()


# ============================================================================
# Project DB Methods
# ============================================================================

def db_save_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert or update a project record."""
    conn = get_connection()
    try:
        pid = project_data.get("id") or uuid4().hex[:8]
        created_at = project_data.get("created_at") or datetime.now().isoformat()
        
        with conn:
            conn.execute("""
                INSERT INTO projects (
                    id, title, description, category, phase, progress, created_at,
                    opportunity_report, launch_assets, deployment_plan, metrics_report
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    description=excluded.description,
                    category=excluded.category,
                    phase=excluded.phase,
                    progress=excluded.progress,
                    opportunity_report=excluded.opportunity_report,
                    launch_assets=excluded.launch_assets,
                    deployment_plan=excluded.deployment_plan,
                    metrics_report=excluded.metrics_report
            """, (
                pid,
                project_data.get("title", ""),
                project_data.get("description", ""),
                project_data.get("category", "General"),
                project_data.get("phase", "IDEA_INPUT"),
                float(project_data.get("progress", 0.0)),
                created_at,
                json.dumps(project_data.get("opportunity_report")) if isinstance(project_data.get("opportunity_report"), dict) else project_data.get("opportunity_report"),
                json.dumps(project_data.get("launch_assets")) if isinstance(project_data.get("launch_assets"), dict) else project_data.get("launch_assets"),
                json.dumps(project_data.get("deployment_plan")) if isinstance(project_data.get("deployment_plan"), dict) else project_data.get("deployment_plan"),
                json.dumps(project_data.get("metrics_report")) if isinstance(project_data.get("metrics_report"), dict) else project_data.get("metrics_report"),
            ))
        project_data["id"] = pid
        project_data["created_at"] = created_at
        return project_data
    finally:
        conn.close()


def db_get_all_projects() -> List[Dict[str, Any]]:
    """Retrieve all projects from the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
        projects = []
        for r in rows:
            p = dict(r)
            for json_field in ["opportunity_report", "launch_assets", "deployment_plan", "metrics_report"]:
                if p[json_field] and isinstance(p[json_field], str):
                    try:
                        p[json_field] = json.loads(p[json_field])
                    except Exception:
                        pass
            projects.append(p)
        return projects
    finally:
        conn.close()


def db_get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single project by ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not row:
            return None
        p = dict(row)
        for json_field in ["opportunity_report", "launch_assets", "deployment_plan", "metrics_report"]:
            if p[json_field] and isinstance(p[json_field], str):
                try:
                    p[json_field] = json.loads(p[json_field])
                except Exception:
                    pass
        return p
    finally:
        conn.close()


def db_delete_project(project_id: str) -> bool:
    """Delete a project record."""
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()
