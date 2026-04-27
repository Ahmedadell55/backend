from typing import List, Optional, Dict, Any
import math
from business.models.graph import City, Node
from core.city_instance import get_city


class SearchService:
    def __init__(self, city=None):
        # يقبل class أو instance أو None
        pass

    def _get_city(self) -> City:
        return get_city()

    def find_nodes_by_type(self, node_type: str) -> List[Node]:
        city = self._get_city()
        return [n for n in city.nodes.values() if n.type == node_type]

    def search_nodes_by_name(self, query: str) -> List[Node]:
        if not query:
            return []
        city = self._get_city()
        q = query.strip().lower()
        return [n for n in city.nodes.values() if q in n.name.lower()]

    def get_node_type_counts(self) -> Dict[str, int]:
        city = self._get_city()
        counts = {}
        for node in city.nodes.values():
            counts[node.type] = counts.get(node.type, 0) + 1
        return counts

    def get_supported_commands(self) -> List[str]:
        return [
            "find hospital", "find school", "find mosque",
            "find parking", "find gas", "search <name>",
            "stats", "nodes count"
        ]

    async def process_query(self, text: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        text_lower = text.strip().lower()
        city = self._get_city()

        # بحث بالنوع
        for node_type in ["hospital", "school", "mosque", "parking", "gas", "house", "office", "mall", "park", "police", "pharmacy", "restaurant", "factory", "signal"]:
            if node_type in text_lower:
                results = self.find_nodes_by_type(node_type)
                return {
                    "query": text,
                    "type": "node_search",
                    "results": [{"id": n.id, "name": n.name, "type": n.type} for n in results],
                    "count": len(results)
                }

        # بحث بالاسم
        results = self.search_nodes_by_name(text)
        if results:
            return {
                "query": text,
                "type": "name_search",
                "results": [{"id": n.id, "name": n.name, "type": n.type} for n in results],
                "count": len(results)
            }

        # إحصائيات
        if any(w in text_lower for w in ["stats", "count", "كم", "عدد", "إحصاء"]):
            return {
                "query": text,
                "type": "stats",
                "results": {
                    "nodes": len(city.nodes),
                    "edges": len(city.edges),
                    "types": self.get_node_type_counts()
                }
            }

        return {
            "query": text,
            "type": "no_results",
            "results": [],
            "message": "لا توجد نتائج. جرّب: find hospital, find school"
        }
