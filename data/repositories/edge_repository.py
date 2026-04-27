# data/repositories/edge_repository.py
"""
Repository للتعامل مع جدول edges في Supabase
"""

from typing import List, Dict, Any, Optional
from data.supabase_client import get_supabase
from core import DatabaseError, EdgeNotFoundError


class EdgeRepository:
    """كل عمليات الـ CRUD الخاصة بالحواف (Edges)"""

    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "edges"

    async def create(self, edge_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        إنشاء حافة جديدة (طريق بين عقدتين)
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .insert(edge_data)
                .execute()
            )
            return result.data[0] if result.data else None

        except Exception as e:
            raise DatabaseError("create edge", str(e))

    async def get_all(self, project_id: str) -> List[Dict[str, Any]]:
        """
        جلب كل حواف المشروع
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("project_id", project_id)
                .execute()
            )
            return result.data

        except Exception as e:
            raise DatabaseError("get all edges", str(e))

    async def get_by_id(self, edge_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        """
        جلب حافة معينة بالـ ID
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", edge_id)
                .eq("project_id", project_id)
                .execute()
            )

            return result.data[0] if result.data else None

        except Exception as e:
            raise DatabaseError("get edge by id", str(e))

    async def update_congestion(
        self,
        edge_id: str,
        project_id: str,
        congestion: float
    ) -> Dict[str, Any]:
        """
        تحديث مستوى الازدحام لحافة معينة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .update({"congestion": congestion})
                .eq("id", edge_id)
                .eq("project_id", project_id)
                .execute()
            )

            return result.data[0] if result.data else None

        except Exception as e:
            raise DatabaseError("update congestion", str(e))

    async def delete(self, edge_id: str, project_id: str) -> bool:
        """
        حذف حافة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .delete()
                .eq("id", edge_id)
                .eq("project_id", project_id)
                .execute()
            )

            return len(result.data) > 0

        except Exception as e:
            raise DatabaseError("delete edge", str(e))