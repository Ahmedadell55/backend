import logging
from typing import Optional
from supabase import create_client, Client
from core.config import settings

logger = logging.getLogger(__name__)
_supabase_client: Optional[Client] = None


def init_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logger.info("✅ Supabase connected")
        except Exception as e:
            logger.error(f"❌ Supabase failed: {e}")
            raise RuntimeError(f"Supabase initialization failed: {e}")
    return _supabase_client


def get_supabase() -> Client:
    if _supabase_client is None:
        raise RuntimeError("Supabase not initialized. Call init_supabase() first.")
    return _supabase_client
