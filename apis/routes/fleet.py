# api/routes/fleet.py
"""
Routes لإدارة أسطول المركبات
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict

from apis.dependencies.auth import get_current_user_id
from data.repositories.vehicle_repository import VehicleRepository
from core.exceptions import DatabaseError, VehicleNotFoundError

router = APIRouter(prefix="/fleet", tags=["Fleet"])


# =========================
# Models
# =========================
class VehicleUpdate(BaseModel):
    status: str  # "moving" | "stopped"
    speed: float
    location: Dict[str, float]  # {"lat": x, "lng": y}


# =========================
# Get Vehicles
# =========================
@router.get("/vehicles")
async def get_vehicles(
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = VehicleRepository()

        return await repo.get_all(user_id)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Fleet Stats
# =========================
@router.get("/stats")
async def fleet_stats(
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = VehicleRepository()

        return await repo.get_stats(user_id)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Update Vehicle
# =========================
@router.patch("/vehicles/{vehicle_id}")
async def update_vehicle(
    vehicle_id: str,
    update: VehicleUpdate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = VehicleRepository()

        result = await repo.update_status(
            vehicle_id=vehicle_id,
            user_id=user_id,
            status=update.status,
            speed=update.speed,
            location=update.location
        )

        if not result:
            raise VehicleNotFoundError(vehicle_id)

        return {
            "success": True,
            "message": f"Vehicle {vehicle_id} updated",
            "vehicle": result
        }

    except VehicleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))