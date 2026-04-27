# api/dependencies/auth.py
"""
اعتماديات FastAPI للمصادقة والتحقق من المستخدمين
"""

from fastapi import Header, HTTPException, Depends
from typing import Optional
from supabase import Client

from data.supabase_client import get_supabase
from core.exceptions import InvalidTokenError


# =========================
# 1) Extract Token
# =========================
async def get_token_from_header(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> str:
    """
    استخراج التوكن من الهيدر
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")

    parts = authorization.split()

    # Bearer token
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]

    return authorization


# =========================
# 2) Current User
# =========================
async def get_current_user(
    token: str = Depends(get_token_from_header)
):
    """
    جلب المستخدم الحالي من التوكن
    """
    try:
        supabase: Client = get_supabase()
        user = supabase.auth.get_user(token)

        if not user or not user.user:
            raise InvalidTokenError()

        return user.user

    except InvalidTokenError:
        raise

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# =========================
# 3) User ID only
# =========================
async def get_current_user_id(
    current_user=Depends(get_current_user)
) -> str:
    return current_user.id


# =========================
# 4) Optional User
# =========================
async def optional_user(
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    """
    المستخدم اختياري (public endpoints)
    """
    if not authorization:
        return None

    try:
        token = authorization.replace("Bearer ", "")
        supabase: Client = get_supabase()

        user = supabase.auth.get_user(token)
        return user.user if user and user.user else None

    except Exception:
        return None