# api/routes/auth.py
"""
Routes للمصادقة: تسجيل، دخول، خروج، نسيت كلمة المرور
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from data.supabase_client import get_supabase
from apis.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================
# Models
# =========================
class RegisterRequest(BaseModel):
    email: str   # plain str — Supabase validates email on its own
    password: str
    username: str
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    email: str   # plain str — no pydantic email check
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str   # plain str


class ResetPasswordRequest(BaseModel):
    new_password: str


# =========================
# Register
# =========================
@router.post("/register")
async def register(user_data: RegisterRequest):
    try:
        supabase = get_supabase()

        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "username": user_data.username,
                    "phone": user_data.phone or ""
                }
            }
        })

        if not response.user:
            raise HTTPException(status_code=400, detail="فشل إنشاء الحساب")

        # Return token if session exists (email confirmation disabled in Supabase)
        token = None
        if response.session:
            token = response.session.access_token

        return {
            "success": True,
            "user_id": response.user.id,
            "email": response.user.email,
            "access_token": token,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "username": user_data.username,
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        err = str(e)
        if "already registered" in err or "already exists" in err:
            raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجّل بالفعل — جرّب تسجيل الدخول")
        raise HTTPException(status_code=500, detail=err)


# =========================
# Login
# =========================
@router.post("/login")
async def login(credentials: LoginRequest):
    try:
        supabase = get_supabase()

        result = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })

        if not result.user or not result.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "success": True,
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "user": {
                "id": result.user.id,
                "email": result.user.email,
                "username": result.user.user_metadata.get("username", ""),
                "phone": result.user.user_metadata.get("phone", "")
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        err = str(e)
        if "invalid" in err.lower() or "credentials" in err.lower() or "wrong" in err.lower():
            raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")
        if "email" in err.lower() and "confirm" in err.lower():
            raise HTTPException(status_code=401, detail="يرجى تأكيد بريدك الإلكتروني أولاً")
        raise HTTPException(status_code=401, detail=err)

#========================forget=========================@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    try:
        supabase = get_supabase()
        supabase.auth.reset_password_for_email(
            request.email,
            {
                "redirect_to": f"{settings.FRONTEND_URL}/reset-password"
            }
        )
        return {
            "success": True,
            "message": "Reset email sent"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# =========================
# Reset Password
# =========================
@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    current_user=Depends(get_current_user)
):
    try:
        supabase = get_supabase()

        supabase.auth.update_user({
            "password": request.new_password
        })

        return {
            "success": True,
            "message": "Password updated successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Get current user
# =========================
@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.user_metadata.get("username", ""),
        "phone": current_user.user_metadata.get("phone", "")
    }


# =========================
# Google OAuth
# =========================
from fastapi.responses import RedirectResponse
from core.config import settings

# =========================
# Google OAuth
# =========================
@router.get("/google")
async def google_login():
    try:
        supabase = get_supabase()
        
        result = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                # ✅ بيقول لـ Supabase يرجع على الباك إند مش الفرونت
                
                "redirect_to": f"https://jgoizofoygoewtdrxatx.supabase.co/auth/v1/callback"
            }
        })

        # ✅ بدل ما يرجع JSON، بيعمل redirect مباشرة لـ Google
        return RedirectResponse(url=result.url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# Google OAuth Callback
# =========================
@router.get("/callback")
async def google_callback(code: str):
    try:
        supabase = get_supabase()

        # ✅ بيحول الـ code لـ session
        result = supabase.auth.exchange_code_for_session({"auth_code": code})

        if not result.session:
            raise HTTPException(status_code=400, detail="فشل تسجيل الدخول")

        token = result.session.access_token
        frontend = settings.FRONTEND_URL or "http://localhost:3000"

        # ✅ بيرجع المستخدم للفرونت مع التوكن
        return RedirectResponse(url=f"{frontend}/dashboard?token={token}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
