"""Supabase client wrapper for BuilderForge.

Provides optional auth and data persistence.
Gracefully degrades if Supabase is not configured.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Try to import supabase - fail gracefully if not available
try:
    from supabase import create_client, Client
    _supabase_available = True
except ImportError:
    _supabase_available = False


def get_supabase_client() -> Optional[Any]:
    """Initialise and return a Supabase client if configured."""
    if not _supabase_available:
        return None

    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if not url or not key:
        return None

    try:
        return create_client(url, key)
    except Exception:
        return None


def is_configured() -> bool:
    """Check if Supabase is fully configured."""
    return bool(os.getenv("SUPABASE_URL")) and bool(os.getenv("SUPABASE_KEY"))


def sign_up(email: str, password: str) -> Dict[str, Any]:
    """Register a new user. Returns result dict with success/error."""
    client = get_supabase_client()
    if not client:
        return {"success": False, "error": "Supabase not configured"}

    try:
        resp = client.auth.sign_up({"email": email, "password": password})
        return {"success": True, "user": resp.user}
    except Exception as e:
        return {"success": False, "error": str(e)}


def sign_in(email: str, password: str) -> Dict[str, Any]:
    """Authenticate an existing user."""
    client = get_supabase_client()
    if not client:
        return {"success": False, "error": "Supabase not configured"}

    try:
        resp = client.auth.sign_in_with_password({"email": email, "password": password})
        return {"success": True, "session": resp.session}
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_project(user_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Persist a project record to Supabase."""
    client = get_supabase_client()
    if not client:
        return {"success": False, "error": "Supabase not configured"}

    try:
        resp = client.table("projects").insert({
            "user_id": user_id,
            **project_data
        }).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_projects(user_id: str) -> List[Dict[str, Any]]:
    """Fetch all projects for a user."""
    client = get_supabase_client()
    if not client:
        return []

    try:
        resp = client.table("projects").select("*").eq("user_id", user_id).execute()
        return resp.data if resp.data else []
    except Exception:
        return []
