from typing import List, Dict, Optional
from pydantic import BaseModel


class Node(BaseModel):
    id: str
    name: str
    type: str
    x: float
    y: float
    user_id: Optional[str] = None


class Edge(BaseModel):
    id: str
    source: str
    target: str
    weight: float
    congestion: float = 0.0
    user_id: Optional[str] = None


class City:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges[edge.id] = edge

    def remove_node(self, node_id: str):
        self.nodes.pop(node_id, None)
        to_remove = [eid for eid, e in self.edges.items() if e.source == node_id or e.target == node_id]
        for eid in to_remove:
            self.edges.pop(eid)

    def remove_edge(self, edge_id: str):
        self.edges.pop(edge_id, None)

    def get_neighbors(self, node_id: str) -> List[str]:
        neighbors = []
        for edge in self.edges.values():
            if edge.source == node_id:
                neighbors.append(edge.target)
            elif edge.target == node_id:
                neighbors.append(edge.source)
        return neighbors

    def get_edge_weight(self, u: str, v: str) -> float:
        for edge in self.edges.values():
            if (edge.source == u and edge.target == v) or (edge.source == v and edge.target == u):
                return edge.weight
        return float("inf")

    def get_edge_congestion(self, u: str, v: str) -> float:
        for edge in self.edges.values():
            if (edge.source == u and edge.target == v) or (edge.source == v and edge.target == u):
                return edge.congestion
        return 0.0

    def degree(self, node_id: str) -> int:
        return len(self.get_neighbors(node_id))

    def clear(self):
        self.nodes.clear()
        self.edges.clear()

    @classmethod
    def from_dict(cls, data: dict) -> "City":
        city = cls()
        for n in data.get("nodes", []):
            city.add_node(Node(**n))
        for e in data.get("edges", []):
            city.add_edge(Edge(**e))
        return city

    def to_dict(self) -> dict:
        return {
            "nodes": [n.dict() for n in self.nodes.values()],
            "edges": [e.dict() for e in self.edges.values()]
        }
