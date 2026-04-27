from fastapi import Header, HTTPException, Depends
from typing import Optional
from supabase import Client
from data.supabase_client import get_supabase


# =========================
# Extract Bearer Token (safe)
# =========================
async def get_token_from_header(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")

    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token format")

    return parts[1]


# =========================
# Current User (safe + clean)
# =========================
async def get_current_user(
    token: str = Depends(get_token_from_header)
):
    supabase: Client = get_supabase()

    try:
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return user_response.user

    except Exception:
        raise HTTPException(status_code=401, detail="Authentication failed")


# =========================
# User ID shortcut
# =========================
async def get_current_user_id(
    current_user=Depends(get_current_user)
) -> str:
    return current_user.id


# =========================
# Optional user (safe)
# =========================
async def optional_user(
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) != 2:
        return None

    try:
        supabase: Client = get_supabase()
        user = supabase.auth.get_user(parts[1])
        return user.user if user else None
    except Exception:
        return None
