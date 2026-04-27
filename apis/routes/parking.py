# api/routes/parking.py
"""
Routes لإدارة مواقف السيارات
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from apis.dependencies.auth import get_current_user_id
from data.repositories.parking_repository import ParkingRepository
from core.exceptions import DatabaseError

router = APIRouter(prefix="/parking", tags=["Parking"])


# =========================
# Models
# =========================
class ReserveRequest(BaseModel):
    lot_id: str


# =========================
# Get Available Lots
# =========================
@router.get("/lots")
async def get_available_lots():
    try:
        repo = ParkingRepository()

        return await repo.get_available_lots()

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Reserve Parking
# =========================
@router.post("/reserve")
async def reserve_parking(
    request: ReserveRequest,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = ParkingRepository()

        success = await repo.reserve(request.lot_id, user_id)

        if not success:
            raise HTTPException(
                status_code=400,
                detail="Parking lot not available"
            )

        return {
            "success": True,
            "message": f"Parking lot {request.lot_id} reserved"
        }

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Release Parking
# =========================
@router.post("/release/{lot_id}")
async def release_parking(
    lot_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = ParkingRepository()

        success = await repo.release(lot_id, user_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        return {
            "success": True,
            "message": f"Parking lot {lot_id} released"
        }

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))