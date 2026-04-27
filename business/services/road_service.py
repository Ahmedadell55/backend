"""
Road Service
خدمات توزيع الطرق واقتراح طرق جديدة باستخدام MST (Kruskal)
وتحليل شبكة الطرق
"""

import math
from typing import List, Dict, Tuple

from business.models.graph import City
from business.models.dto import RoadResult, RoadSuggestion
from business.services.analysis_service import AnalysisService


class RoadService:
    """تحسين شبكة الطرق + اقتراح وصلات جديدة"""

    def __init__(self, city: City):
        self.city = city

    # =========================
    # Helpers
    # =========================

    def _distance(self, u: str, v: str) -> float:
        n1, n2 = self.city.nodes[u], self.city.nodes[v]
        return math.hypot(n1.x - n2.x, n1.y - n2.y) / 10.0

    def _get_all_possible_edges(self) -> List[Tuple[float, str, str]]:
        nodes = list(self.city.nodes.keys())
        edges = []

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                edges.append((self._distance(u, v), u, v))

        return sorted(edges, key=lambda x: x[0])

    def _get_length_category(self, d: float) -> str:
        if d < 0.5:
            return "قصير جداً"
        elif d < 1.5:
            return "قصير"
        elif d < 3:
            return "متوسط"
        elif d < 5:
            return "طويل"
        return "طويل جداً"

    # =========================
    # MST (Kruskal)
    # =========================

    async def suggest_roads_with_mst(self) -> RoadResult:
        nodes = list(self.city.nodes.keys())

        if len(nodes) < 2:
            return RoadResult(
                algorithm="MST - Kruskal",
                summary={"error": "Need at least 2 nodes"},
                essential_roads=[],
                suggested_extra_roads=[],
                quality_report={}
            )

        edges = self._get_all_possible_edges()

        # Union-Find
        parent = {n: n for n in nodes}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True

        mst = []

        for dist, u, v in edges:
            if union(u, v):
                mst.append({
                    "source": u,
                    "target": v,
                    "source_name": self.city.nodes[u].name,
                    "target_name": self.city.nodes[v].name,
                    "distance_km": round(dist, 2),
                    "length_category": self._get_length_category(dist)
                })

            if len(mst) == len(nodes) - 1:
                break

        # degree analysis
        degree = {n: 0 for n in nodes}
        for e in mst:
            degree[e["source"]] += 1
            degree[e["target"]] += 1

        dead_ends = [n for n, d in degree.items() if d == 1]

        # extra suggestions
        extra = []
        used = set()

        for e in mst:
            used.add((e["source"], e["target"]))
            used.add((e["target"], e["source"]))

        for dnode in dead_ends:
            for dist, u, v in edges:
                if dnode in (u, v) and (u, v) not in used and dist <= 3:
                    extra.append({
                        "source": u,
                        "target": v,
                        "source_name": self.city.nodes[u].name,
                        "target_name": self.city.nodes[v].name,
                        "distance_km": round(dist, 2),
                        "length_category": self._get_length_category(dist)
                    })
                    break

        essential = [
            RoadSuggestion(**e)
            for e in mst
        ]

        extra_suggestions = [
            RoadSuggestion(**e)
            for e in extra
        ]

        recommendation = (
            "⚠️ شبكة ضعيفة" if len(dead_ends) > len(mst) * 0.3 else
            "📌 تحتاج تحسين" if len(dead_ends) > 2 else
            "✓ ممتازة"
        )

        return RoadResult(
            algorithm="MST - Kruskal",
            summary={
                "nodes": len(nodes),
                "mst_roads": len(mst),
                "extra_roads": len(extra_suggestions),
                "dead_ends": len(dead_ends)
            },
            essential_roads=essential[:10],
            suggested_extra_roads=extra_suggestions[:5],
            quality_report={
                "avg_degree": sum(degree.values()) / len(nodes),
                "connectivity": len(mst) >= len(nodes) - 1,
                "recommendation": recommendation
            }
        )

    # =========================
    # Connectivity Analysis
    # =========================

    async def analyze_connectivity(self) -> Dict:
        analysis = AnalysisService(self.city)

        components = analysis.find_connected_components()
        isolated = analysis.find_isolated_nodes()

        return {
            "connected_components": len(components),
            "isolated_nodes": isolated,
            "is_fully_connected": len(components) == 1,
            "total_nodes": len(self.city.nodes),
            "total_edges": len(self.city.edges)
        }