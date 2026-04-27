"""
خدمات حساب المسارات والخوارزميات:
- BFS (Breadth First Search)
- UCS (Dijkstra)
- A* (A Star)
- Best Path with Congestion
"""

import math
from heapq import heappush, heappop
from collections import deque
from typing import List

from business.models.graph import City
from business.models.dto import PathResult


class PathService:
    """خدمات حساب المسارات في المدينة"""

    def __init__(self, city: City):
        self.city = city

    # =========================
    # Heuristic (A*)
    # =========================
    def _heuristic(self, node: str, target: str) -> float:
        if node not in self.city.nodes or target not in self.city.nodes:
            return 0.0

        dx = self.city.nodes[node].x - self.city.nodes[target].x
        dy = self.city.nodes[node].y - self.city.nodes[target].y
        return math.hypot(dx, dy) / 10.0

    # =========================
    # Distance
    # =========================
    def _calculate_path_distance(self, path: List[str]) -> float:
        total = 0.0
        for i in range(len(path) - 1):
            total += self.city.get_edge_weight(path[i], path[i + 1])
        return total

    # =========================
    # BFS (optimized)
    # =========================
    def bfs(self, start: str, end: str) -> PathResult:
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()

            if node == end:
                return PathResult(
                    algorithm="BFS",
                    path=path,
                    total_distance_km=round(self._calculate_path_distance(path), 2),
                    description="أقصر طريق بعدد التقاطعات",
                    num_edges=len(path) - 1
                )

            for neighbor in self.city.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        raise ValueError(f"No path found from {start} to {end}")

    # =========================
    # UCS (Dijkstra)
    # =========================
    def ucs(self, start: str, end: str) -> PathResult:
        pq = [(0, start, [start])]
        visited_cost = {start: 0}

        while pq:
            cost, node, path = heappop(pq)

            if node == end:
                return PathResult(
                    algorithm="UCS",
                    path=path,
                    total_distance_km=round(cost, 2),
                    description="أقصر طريق بالمسافة الفعلية",
                    num_edges=len(path) - 1
                )

            for neighbor in self.city.get_neighbors(node):
                new_cost = cost + self.city.get_edge_weight(node, neighbor)

                if neighbor not in visited_cost or new_cost < visited_cost[neighbor]:
                    visited_cost[neighbor] = new_cost
                    heappush(pq, (new_cost, neighbor, path + [neighbor]))

        raise ValueError(f"No path found from {start} to {end}")

    # =========================
    # A* Algorithm
    # =========================
    def astar(self, start: str, end: str) -> PathResult:
        pq = [(self._heuristic(start, end), 0, start, [start])]
        g_score = {start: 0}

        while pq:
            _, cost, node, path = heappop(pq)

            if node == end:
                return PathResult(
                    algorithm="A*",
                    path=path,
                    total_distance_km=round(cost, 2),
                    description="أسرع طريق باستخدام A*",
                    num_edges=len(path) - 1
                )

            for neighbor in self.city.get_neighbors(node):
                tentative = cost + self.city.get_edge_weight(node, neighbor)

                if neighbor not in g_score or tentative < g_score[neighbor]:
                    g_score[neighbor] = tentative
                    f_score = tentative + self._heuristic(neighbor, end)
                    heappush(pq, (f_score, tentative, neighbor, path + [neighbor]))

        raise ValueError(f"No path found from {start} to {end}")

    # =========================
    # Best Path (Congestion-aware)
    # =========================
    def best_path_with_congestion(self, start: str, end: str) -> PathResult:

        def heuristic(node: str, target: str) -> float:
            return self._heuristic(node, target) * 1.2

        def edge_cost(u: str, v: str) -> float:
            dist = self.city.get_edge_weight(u, v)
            congestion = self.city.get_edge_congestion(u, v)
            return dist * (1 + congestion * 2)

        pq = [(heuristic(start, end), 0, start, [start])]
        g_score = {start: 0}

        while pq:
            _, cost, node, path = heappop(pq)

            if node == end:
                return PathResult(
                    algorithm="Best Path",
                    path=path,
                    total_distance_km=round(cost, 2),
                    description="أفضل طريق مع مراعاة الزحمة",
                    num_edges=len(path) - 1
                )

            for neighbor in self.city.get_neighbors(node):
                new_cost = cost + edge_cost(node, neighbor)

                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    f_score = new_cost + heuristic(neighbor, end)
                    heappush(pq, (f_score, new_cost, neighbor, path + [neighbor]))

        raise ValueError(f"No path found from {start} to {end}")