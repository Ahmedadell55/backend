# data/repositories/project_repository.py
"""
Repository للتعامل مع جدول projects في Supabase
"""

from typing import List, Dict, Any, Optional
from data.supabase_client import get_supabase
from core import DatabaseError, ProjectNotFoundError


class ProjectRepository:
    """كل عمليات الـ CRUD الخاصة بالمشاريع (metadata فقط)"""

    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "projects"

    async def create(self, user_id: str, name: str) -> Dict[str, Any]:
        """
        إنشاء مشروع جديد (بدون nodes/edges لأنهم جداول منفصلة)
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .insert({
                    "user_id": user_id,
                    "name": name
                })
                .execute()
            )

            return result.data[0] if result.data else None

        except Exception as e:
            raise DatabaseError("create project", str(e))

    async def get_all(self, user_id: str) -> List[Dict[str, Any]]:
        """
        جلب كل مشاريع المستخدم
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            return result.data

        except Exception as e:
            raise DatabaseError("get all projects", str(e))

    async def get_by_id(self, project_id: str, user_id: str) -> Dict[str, Any]:
        """
        جلب مشروع معين
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", project_id)
                .eq("user_id", user_id)
                .execute()
            )

            if not result.data:
                raise ProjectNotFoundError(project_id)

            return result.data[0]

        except ProjectNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("get project by id", str(e))

    async def update(self, project_id: str, user_id: str, name: str) -> Dict[str, Any]:
        """
        تحديث اسم المشروع فقط
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .update({
                    "name": name
                })
                .eq("id", project_id)
                .eq("user_id", user_id)
                .execute()
            )

            if not result.data:
                raise ProjectNotFoundError(project_id)

            return result.data[0]

        except ProjectNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("update project", str(e))

    async def delete(self, project_id: str, user_id: str) -> bool:
        """
        حذف مشروع
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .delete()
                .eq("id", project_id)
                .eq("user_id", user_id)
                .execute()
            )

            return len(result.data) > 0

        except Exception as e:
            raise DatabaseError("delete project", str(e))