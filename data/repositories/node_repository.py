# data/repositories/node_repository.py
"""
Repository للتعامل مع جدول nodes في Supabase
"""

from typing import List, Dict, Any, Optional
from data.supabase_client import get_supabase
from core import (
    DatabaseError,
    NodeNotFoundError
)


class NodeRepository:
    """كل عمليات الـ CRUD الخاصة بالعقد (Nodes)"""

    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "nodes"

    async def create(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        إنشاء عقدة جديدة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .insert(node_data)
                .execute()
            )
            return result.data[0] if result.data else None

        except Exception as e:
            raise DatabaseError("create node", str(e))

    async def get_all(self, project_id: str) -> List[Dict[str, Any]]:
        """
        جلب كل عقد المشروع
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
            raise DatabaseError("get all nodes", str(e))

    async def get_by_id(self, node_id: str, project_id: str) -> Dict[str, Any]:
        """
        جلب عقدة معينة بالـ ID
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", node_id)
                .eq("project_id", project_id)
                .execute()
            )

            if not result.data:
                raise NodeNotFoundError(node_id)

            return result.data[0]

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("get node by id", str(e))

    async def update(
        self,
        node_id: str,
        project_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        تحديث بيانات عقدة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .update(updates)
                .eq("id", node_id)
                .eq("project_id", project_id)
                .execute()
            )

            if not result.data:
                raise NodeNotFoundError(node_id)

            return result.data[0]

        except NodeNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("update node", str(e))

    async def delete(self, node_id: str, project_id: str) -> bool:
        """
        حذف عقدة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .delete()
                .eq("id", node_id)
                .eq("project_id", project_id)
                .execute()
            )

            return len(result.data) > 0

        except Exception as e:
            raise DatabaseError("delete node", str(e))