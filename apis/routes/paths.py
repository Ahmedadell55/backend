# api/routes/paths.py

from fastapi import APIRouter, HTTPException, Depends

from business.services.path_service import PathService
from business.models.graph import City
from business.models.dto import PathRequest, PathResult
from core.city_instance import get_city as get_city_instance

router = APIRouter(prefix="/paths", tags=["Path Algorithms"])


# =========================
# PathService Dependency
# يستخدم city_instance في الذاكرة
# =========================
def get_path_service():
    city = get_city_instance()
    return PathService(city)


# =========================
# Shortest Path
# =========================
@router.post("/shortest", response_model=PathResult)
async def shortest_path(
    request: PathRequest,
    path_service: PathService = Depends(get_path_service)
):
    try:
        algo = request.algorithm.lower()
        if algo in ("bfs",):
            result = path_service.bfs(request.start, request.end)
        elif algo in ("astar", "a*"):
            result = path_service.astar(request.start, request.end)
        else:  # ucs / dijkstra / default
            result = path_service.ucs(request.start, request.end)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Best Path (congestion-aware)
# =========================
@router.post("/best", response_model=PathResult)
async def best_path(
    request: PathRequest,
    path_service: PathService = Depends(get_path_service)
):
    try:
        return path_service.best_path_with_congestion(request.start, request.end)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
