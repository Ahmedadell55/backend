# data/repositories/__init__.py
from data.repositories.node_repository import NodeRepository
from data.repositories.edge_repository import EdgeRepository
from data.repositories.project_repository import ProjectRepository
from data.repositories.vehicle_repository import VehicleRepository
from data.repositories.parking_repository import ParkingRepository
from data.supabase_client import get_supabase
__all__ = [
    "get_supabase",
    "NodeRepository",
    "EdgeRepository",
    "ProjectRepository",
    "VehicleRepository",
    "ParkingRepository"
]