"""
Data Transfer Objects (DTOs)
نماذج نقل البيانات بين الـ API والـ Services
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# =========================
# Path API
# =========================
class PathRequest(BaseModel):
    start: str
    end: str
    algorithm: str = "ucs"  # bfs | ucs | astar


class PathResult(BaseModel):
    algorithm: str
    path: List[str]
    total_distance_km: float
    description: str
    heuristic_used: Optional[str] = None
    num_edges: Optional[int] = None


# =========================
# Graph API
# =========================
class CreateNodeRequest(BaseModel):
    id: str
    name: str
    type: str
    x: float
    y: float


class CreateEdgeRequest(BaseModel):
    id: str
    source: str
    target: str
    weight: float
    congestion: float = 0.0


class MoveNodeRequest(BaseModel):
    node_id: str
    x: float
    y: float


class UpdateCongestionRequest(BaseModel):
    edge_id: str
    congestion: float


# =========================
# Facility / Analysis
# =========================
class FacilityRequest(BaseModel):
    facility_type: str
    num_facilities: int
    algorithm: str = "hill_climbing"


class FacilityLocation(BaseModel):
    id: str
    name: str
    type: Optional[str] = None


class FacilityResult(BaseModel):
    algorithm: str
    facility_type: str
    locations: List[FacilityLocation]
    total_cost: float
    description: str


class RoadSuggestion(BaseModel):
    source: str
    target: str
    source_name: str
    target_name: str
    distance_km: float


class RoadResult(BaseModel):
    algorithm: str
    summary: Dict[str, Any]
    essential_roads: List[RoadSuggestion]
    suggested_extra_roads: List[RoadSuggestion]
    quality_report: Dict[str, Any]

class NodeImportance(BaseModel):
    node_id: str
    score: float


class AnalysisResult(BaseModel):
    important_nodes: List[NodeImportance]
    summary: str