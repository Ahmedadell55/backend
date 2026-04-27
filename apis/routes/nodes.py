# api/routes/nodes.py
"""
Routes لإدارة العقد (Nodes) في الرسم البياني
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from apis.dependencies.auth import get_current_user_id
from data.repositories.node_repository import NodeRepository
from business.models.graph import Node
from core.exceptions import NodeNotFoundError, DatabaseError

router = APIRouter(prefix="/nodes", tags=["Nodes"])


# =========================
# Create Node
# =========================
@router.post("/", response_model=Node)
async def create_node(
    node: Node,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = NodeRepository()

        node_data = node.dict()
        node_data["user_id"] = user_id

        result = await repo.create(node_data)

        return Node(**result)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Get All Nodes
# =========================
@router.get("/", response_model=List[Node])
async def get_all_nodes(
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = NodeRepository()

        nodes = await repo.get_all(user_id)

        return [Node(**node) for node in nodes]

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Get Node by ID
# =========================
@router.get("/{node_id}", response_model=Node)
async def get_node(
    node_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = NodeRepository()

        node = await repo.get_by_id(node_id, user_id)

        return Node(**node)

    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Update Node
# =========================
@router.put("/{node_id}", response_model=Node)
async def update_node(
    node_id: str,
    node: Node,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = NodeRepository()

        updates = node.dict(exclude={"id"})

        result = await repo.update(node_id, user_id, updates)

        return Node(**result)

    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Delete Node
# =========================
@router.delete("/{node_id}")
async def delete_node(
    node_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        repo = NodeRepository()

        await repo.delete(node_id, user_id)

        return {
            "success": True,
            "message": f"Node {node_id} deleted"
        }

    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))