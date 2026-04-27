# api/routes/projects.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict

from apis.dependencies.auth import get_current_user_id
from data.file_repository import FileRepository
from business.services.projectservice import ProjectService
from core.exceptions import DatabaseError, FileOperationError

router = APIRouter(prefix="/projects", tags=["Projects"])


# =========================
# Models
# =========================
class CreateProjectRequest(BaseModel):
    name: str
    nodes: List[Dict] = []
    edges: List[Dict] = []


class UpdateProjectRequest(BaseModel):
    name: str
    nodes: List[Dict]
    edges: List[Dict]


# =========================
# Dependencies
# =========================
def get_project_service():
    return ProjectService()

def get_file_repo():
    return FileRepository()


# =========================
# CREATE
# =========================
@router.post("/")
async def create_project(
    request: CreateProjectRequest,
    user_id: str = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service)
):
    return await service.create_project(
        user_id,
        request.name,
        request.nodes,
        request.edges
    )


# =========================
# READ
# =========================
@router.get("/")
async def get_projects(
    user_id: str = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service)
):
    return await service.get_user_projects(user_id)


# =========================
# UPDATE
# =========================
@router.put("/{project_id}")
async def update_project(
    project_id: str,
    request: UpdateProjectRequest,
    user_id: str = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service)
):

    result = await service.update_project(
        project_id,
        user_id,
        request.name,
        request.nodes,
        request.edges
    )

    if not result:
        raise HTTPException(status_code=404, detail="Project not found")

    return result


# =========================
# DELETE
# =========================
@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service)
):

    await service.delete_project(project_id, user_id)

    return {"success": True, "message": "Deleted"}


# =========================
# SAVE LOCAL (.dar)
# =========================
@router.post("/save-local")
async def save_local(
    filename: str,
    user_id: str = Depends(get_current_user_id),
    service: ProjectService = Depends(get_project_service),
    file_repo: FileRepository = Depends(get_file_repo)
):

    data = await service.export_current_graph(user_id)
    path = file_repo.save_project(filename, data)

    return {"success": True, "path": path}


# =========================
# LOAD LOCAL
# =========================
@router.post("/load-local")
async def load_local(
    filename: str,
    service: ProjectService = Depends(get_project_service),
    file_repo: FileRepository = Depends(get_file_repo)
):

    data = file_repo.load_project(filename)
    await service.import_graph(data)

    return {"success": True, "message": "Loaded"}


# =========================
# LIST LOCAL
# =========================
@router.get("/local")
async def list_local(
    file_repo: FileRepository = Depends(get_file_repo)
):

    return {"projects": file_repo.list_projects()}