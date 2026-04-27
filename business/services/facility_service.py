"""
Facility Service - Smart City Optimization
- Hill Climbing
- Simulated Annealing
"""

import random
import math
from typing import List

from business.models.graph import City
from business.models.dto import FacilityResult, FacilityLocation


class FacilityService:
    def __init__(self, city: City):
        self.city = city

    # =========================
    # Cost Function (Coverage)
    # =========================
    def _coverage_cost(self, centers: List[str]) -> float:
        nodes = list(self.city.nodes)
        total = 0.0

        for node in nodes:
            if not centers:
                return float("inf")

            min_dist = min(
                self._euclidean(node, c)
                for c in centers
                if c in self.city.nodes
            )

            total += min_dist

        return total

    # =========================
    # Distance
    # =========================
    def _euclidean(self, a: str, b: str) -> float:
        na = self.city.nodes[a]
        nb = self.city.nodes[b]
        return math.hypot(na.x - nb.x, na.y - nb.y) / 10.0

    # =========================
    # Hill Climbing
    # =========================
    async def hill_climbing(self, facility_type: str, k: int) -> FacilityResult:
        nodes = list(self.city.nodes)

        if len(nodes) == 0:
            return self._empty(facility_type, "Hill Climbing")

        k = min(k, len(nodes))
        current = random.sample(nodes, k)
        current_cost = self._coverage_cost(current)

        improved = True
        iterations = 0

        while improved and iterations < 300:
            improved = False

            for i in range(k):
                for candidate in nodes:
                    if candidate in current:
                        continue

                    new = current.copy()
                    new[i] = candidate

                    cost = self._coverage_cost(new)

                    if cost < current_cost:
                        current = new
                        current_cost = cost
                        improved = True
                        break

                if improved:
                    break

            iterations += 1

        return self._build_result(
            facility_type,
            "Hill Climbing",
            current,
            current_cost,
            iterations
        )

    # =========================
    # Simulated Annealing
    # =========================
    async def simulated_annealing(self, facility_type: str, k: int) -> FacilityResult:
        nodes = list(self.city.nodes)

        if len(nodes) == 0:
            return self._empty(facility_type, "Simulated Annealing")

        k = min(k, len(nodes))

        current = random.sample(nodes, k)
        current_cost = self._coverage_cost(current)

        best = current.copy()
        best_cost = current_cost

        T = 100.0
        alpha = 0.95

        iterations = 0

        while T > 0.01 and iterations < 800:
            new = current.copy()

            idx = random.randint(0, k - 1)
            candidates = [n for n in nodes if n not in new]

            if candidates:
                new[idx] = random.choice(candidates)

                cost = self._coverage_cost(new)
                delta = cost - current_cost

                if delta < 0 or random.random() < math.exp(-delta / T):
                    current = new
                    current_cost = cost

                    if cost < best_cost:
                        best = new.copy()
                        best_cost = cost

            T *= alpha
            iterations += 1

        return self._build_result(
            facility_type,
            "Simulated Annealing",
            best,
            best_cost,
            iterations
        )

    # =========================
    # Helpers
    # =========================
    def _build_result(self, ftype, algo, centers, cost, iterations):
        locations = [
            FacilityLocation(
                id=n,
                name=self.city.nodes[n].name,
                type=ftype
            )
            for n in centers
        ]

        return FacilityResult(
            algorithm=algo,
            facility_type=ftype,
            locations=locations,
            total_cost=round(cost, 2),
            description=f"{algo} optimized {len(centers)} facilities in {iterations} iterations"
        )

    def _empty(self, ftype, algo):
        return FacilityResult(
            algorithm=algo,
            facility_type=ftype,
            locations=[],
            total_cost=0,
            description="No nodes available"
        )