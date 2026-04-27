# api/routes/edges.py
"""
Routes لإدارة الحواف (Edges) في الرسم البياني
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel

from apis.dependencies.auth import get_current_user_id
from data.repositories.edge_repository import EdgeRepository
from business.models.graph import Edge
from core.exceptions import DatabaseError, EdgeNotFoundError

router = APIRouter(prefix="/edges", tags=["Edges"])


# =========================
# Models
# =========================
class CongestionUpdate(BaseModel):
    congestion: float


# =========================
# Create Edge
# =========================
@router.post("/", response_model=Edge)
async def create_edge(
    edge: Edge,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = EdgeRepository()

        edge_data = edge.dict()
        edge_data["user_id"] = user_id

        result = await repo.create(edge_data)

        return Edge(**result)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Get All Edges
# =========================
@router.get("/", response_model=List[Edge])
async def get_all_edges(
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = EdgeRepository()

        edges = await repo.get_all(user_id)

        return [Edge(**edge) for edge in edges]

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Update Congestion
# =========================
@router.patch("/{edge_id}/congestion")
async def update_congestion(
    edge_id: str,
    update: CongestionUpdate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = EdgeRepository()

        # clamp value بين 0 و 1
        congestion = max(0.0, min(1.0, update.congestion))

        result = await repo.update_congestion(
            edge_id,
            user_id,
            congestion
        )

        if not result:
            raise EdgeNotFoundError(edge_id)

        return {
            "success": True,
            "edge_id": edge_id,
            "congestion": congestion
        }

    except EdgeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Delete Edge
# =========================
@router.delete("/{edge_id}")
async def delete_edge(
    edge_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = EdgeRepository()

        await repo.delete(edge_id, user_id)

        return {
            "success": True,
            "message": f"Edge {edge_id} deleted"
        }

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))