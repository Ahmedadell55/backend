# data/repositories/parking_repository.py
"""
Repository للتعامل مع جدول parking في Supabase
"""

from typing import List, Dict, Any
from datetime import datetime
from data.supabase_client import get_supabase
from core import DatabaseError


class ParkingRepository:
    """كل عمليات مواقف السيارات"""

    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "parking_lots"

    async def get_available_lots(self) -> List[Dict[str, Any]]:
        """
        جلب جميع المواقف المتاحة
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("is_available", True)
                .execute()
            )
            return result.data
        except Exception as e:
            raise DatabaseError("get available parking lots", str(e))

    async def reserve(self, lot_id: str, user_id: str) -> bool:
        """
        حجز موقف سيارات
        """
        try:
            # التأكد إن الموقف موجود ومتاح
            lot = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("id", lot_id)
                .eq("is_available", True)
                .execute()
            )

            if not lot.data:
                return False

            # تنفيذ الحجز
            result = (
                self.supabase.table(self.table_name)
                .update({
                    "is_available": False,
                    "reserved_by": user_id,
                    "reserved_at": datetime.utcnow().isoformat()
                })
                .eq("id", lot_id)
                .execute()
            )

            return len(result.data) > 0

        except Exception as e:
            raise DatabaseError("reserve parking lot", str(e))

    async def release(self, lot_id: str, user_id: str) -> bool:
        """
        إلغاء حجز موقف (عند المغادرة)
        """
        try:
            result = (
                self.supabase.table(self.table_name)
                .update({
                    "is_available": True,
                    "reserved_by": None,
                    "reserved_at": None
                })
                .eq("id", lot_id)
                .eq("reserved_by", user_id)
                .execute()
            )

            return len(result.data) > 0

        except Exception as e:
            raise DatabaseError("release parking lot", str(e))