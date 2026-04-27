# data/repositories/vehicle_repository.py
"""
Repository للتعامل مع جدول vehicles في Supabase
"""

from typing import List, Dict, Any
from data.supabase_client import get_supabase
from core import DatabaseError


class VehicleRepository:
    """كل عمليات الأسطول والمركبات"""
    
    def __init__(self):
        self.supabase = get_supabase()
        self.table_name = "vehicles"
    
    async def get_all(self, user_id: str) -> List[Dict[str, Any]]:
        """
        جلب كل مركبات المستخدم
        """
        try:
            result = self.supabase.table(self.table_name) \
                .select("*") \
                .eq("user_id", user_id) \
                .execute()
            return result.data
        except Exception as e:
            raise DatabaseError("get all vehicles", str(e))
    
    async def update_status(self, vehicle_id: str, user_id: str, status: str, speed: float, location: Dict) -> Dict[str, Any]:
        """
        تحديث حالة مركبة (موقع، سرعة، حالة)
        """
        try:
            result = self.supabase.table(self.table_name) \
                .update({
                    "status": status,
                    "speed": speed,
                    "location": location,
                    "last_update": "now()"
                }) \
                .eq("id", vehicle_id) \
                .eq("user_id", user_id) \
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise DatabaseError("update vehicle status", str(e))
    
    async def get_stats(self, user_id: str) -> Dict[str, Any]:
        """
        إحصائيات عن الأسطول (عدد المركبات، المتحركة، الواقفة)
        """
        try:
            vehicles = await self.get_all(user_id)
            total = len(vehicles)
            moving = len([v for v in vehicles if v.get("status") == "moving"])
            
            return {
                "total_vehicles": total,
                "moving": moving,
                "stopped": total - moving
            }
        except Exception as e:
            raise DatabaseError("get fleet stats", str(e))