from typing import List, Dict, Any, Optional
import uuid
from supabase import create_client

from core.config import settings


class ProjectService:
    def __init__(self):
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    # =========================
    # Create Project
    # =========================
    async def create_project(self, user_id: str, name: str, nodes: List[Dict], edges: List[Dict]):

        project_id = str(uuid.uuid4())

        project = {
            "id": project_id,
            "user_id": user_id,
            "name": name
        }

        # insert project
        self.supabase.table("projects").insert(project).execute()

        # insert nodes
        for node in nodes:
            node["project_id"] = project_id
            self.supabase.table("nodes").insert(node).execute()

        # insert edges
        for edge in edges:
            edge["project_id"] = project_id
            self.supabase.table("edges").insert(edge).execute()

        return project

    # =========================
    # Get Projects
    # =========================
    async def get_user_projects(self, user_id: str):

        res = self.supabase.table("projects") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        return res.data

    # =========================
    # Update Project
    # =========================
    async def update_project(self, project_id: str, user_id: str, name: str, nodes: List[Dict], edges: List[Dict]):

        # update project name
        self.supabase.table("projects") \
            .update({"name": name}) \
            .eq("id", project_id) \
            .eq("user_id", user_id) \
            .execute()

        # delete old nodes/edges
        self.supabase.table("nodes").delete().eq("project_id", project_id).execute()
        self.supabase.table("edges").delete().eq("project_id", project_id).execute()

        # re-insert
        for node in nodes:
            node["project_id"] = project_id
            self.supabase.table("nodes").insert(node).execute()

        for edge in edges:
            edge["project_id"] = project_id
            self.supabase.table("edges").insert(edge).execute()

        return {"success": True}

    # =========================
    # Delete Project
    # =========================
    async def delete_project(self, project_id: str, user_id: str):

        self.supabase.table("nodes").delete().eq("project_id", project_id).execute()
        self.supabase.table("edges").delete().eq("project_id", project_id).execute()

        self.supabase.table("projects") \
            .delete() \
            .eq("id", project_id) \
            .eq("user_id", user_id) \
            .execute()

        return True

    # =========================
    # Export Graph
    # =========================
    async def export_current_graph(self, user_id: str):

        projects = await self.get_user_projects(user_id)

        for p in projects:
            nodes = self.supabase.table("nodes").select("*").eq("project_id", p["id"]).execute()
            edges = self.supabase.table("edges").select("*").eq("project_id", p["id"]).execute()

            p["nodes"] = nodes.data
            p["edges"] = edges.data

        return {
            "user_id": user_id,
            "projects": projects
        }

    # =========================
    # Import Graph
    # =========================
    async def import_graph(self, data: Dict[str, Any]):

        for project in data.get("projects", []):

            self.supabase.table("projects").upsert({
                "id": project["id"],
                "user_id": project["user_id"],
                "name": project["name"]
            }).execute()

            for node in project.get("nodes", []):
                node["project_id"] = project["id"]
                self.supabase.table("nodes").insert(node).execute()

            for edge in project.get("edges", []):
                edge["project_id"] = project["id"]
                self.supabase.table("edges").insert(edge).execute()

        return True