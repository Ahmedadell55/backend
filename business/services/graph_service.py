"""
GraphService
مسؤول عن CRUD على الجراف (Nodes / Edges)
"""

from typing import List, Optional
from business.models.graph import City, Node, Edge


class GraphService:
    """إدارة الرسم البياني (City Graph)"""

    def __init__(self, city: City):
        self.city = city

    # ======================
    # Nodes
    # ======================

    def add_node(self, node: Node) -> Node:
        if node.id in self.city.nodes:
            raise ValueError("Node already exists")

        self.city.add_node(node)
        return node

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.city.nodes.get(node_id)

    def get_all_nodes(self) -> List[Node]:
        return list(self.city.nodes.values())

    def update_node(self, node_id: str, **updates) -> Node:
        node = self.city.nodes.get(node_id)
        if not node:
            raise ValueError("Node not found")

        for k, v in updates.items():
            if hasattr(node, k) and k != "id":
                setattr(node, k, v)

        return node

    def move_node(self, node_id: str, x: float, y: float) -> Node:
        node = self.city.nodes.get(node_id)
        if not node:
            raise ValueError("Node not found")

        node.x = x
        node.y = y
        return node

    def delete_node(self, node_id: str) -> bool:
        if node_id not in self.city.nodes:
            return False

        self.city.remove_node(node_id)
        return True

    # ======================
    # Edges
    # ======================

    def add_edge(self, edge: Edge) -> Edge:
        if edge.source not in self.city.nodes or edge.target not in self.city.nodes:
            raise ValueError("Invalid nodes for edge")

        if self.get_edge_between(edge.source, edge.target):
            raise ValueError("Edge already exists")

        self.city.add_edge(edge)
        return edge

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        return self.city.edges.get(edge_id)

    def get_edge_between(self, u: str, v: str) -> Optional[Edge]:
        for e in self.city.edges.values():
            if (e.source == u and e.target == v) or (e.source == v and e.target == u):
                return e
        return None

    def get_all_edges(self) -> List[Edge]:
        return list(self.city.edges.values())

    def update_edge(self, edge_id: str, **updates) -> Edge:
        edge = self.city.edges.get(edge_id)
        if not edge:
            raise ValueError("Edge not found")

        for k, v in updates.items():
            if hasattr(edge, k) and k != "id":
                setattr(edge, k, v)

        return edge

    def update_congestion(self, edge_id: str, congestion: float) -> Edge:
        edge = self.city.edges.get(edge_id)
        if not edge:
            raise ValueError("Edge not found")

        edge.congestion = max(0.0, min(1.0, congestion))
        return edge

    def delete_edge(self, edge_id: str) -> bool:
        if edge_id not in self.city.edges:
            return False

        self.city.remove_edge(edge_id)
        return True

    # ======================
    # Stats
    # ======================

    def get_stats(self) -> dict:
        nodes = len(self.city.nodes)
        edges = len(self.city.edges)

        if nodes == 0:
            return {
                "nodes": 0,
                "edges": 0,
                "avg_degree": 0,
                "max_degree": 0
            }

        degrees = [self.city.degree(n) for n in self.city.nodes]

        return {
            "nodes": nodes,
            "edges": edges,
            "avg_degree": round(sum(degrees) / nodes, 2),
            "max_degree": max(degrees)
        }

    def clear(self):
        self.city.clear()