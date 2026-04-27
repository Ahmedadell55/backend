# core/utils.py

import math
import hashlib
import uuid
from typing import List, TypeVar

T = TypeVar("T")


# =========================
# 1) Distance Calculation
# =========================
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    حساب المسافة الإقليدية بين نقطتين (مفيد للـ graph / roads)
    """
    return math.hypot(x2 - x1, y2 - y1)


# =========================
# 2) Generate Unique ID
# =========================
def generate_id(prefix: str = "") -> str: # for nodes , roads , projects
    """
    توليد ID فريد لأي عنصر (node, road, project...)
    """
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# =========================
# 3) Hashing (API Keys ONLY)
# =========================
def hash_string(text: str) -> str:
    """
    استخدام آمن فقط لـ:
    - API keys
    - caching keys
    ❌ NOT for passwords
    """
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# =========================
# 4) Chunking Large Lists
# =========================
def chunk_list(lst: List[T], chunk_size: int) -> List[List[T]]:
    """
    تقسيم قائمة كبيرة إلى أجزاء صغيرة (batch processing)
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]