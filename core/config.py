import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    PROJECTS_DIR: str = "saved_projects"
    APP_NAME: str = "Darb SmartCity API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    # ⬇️ هتحطه في Railway Variables بعد ما تاخد رابط Netlify
    FRONTEND_URL: str = "https://graceful-marigold-8eacf9.netlify.app"

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
        if self.FRONTEND_URL:
            origins.append(self.FRONTEND_URL)
        return origins

    def ensure_directories(self):
        os.makedirs(self.PROJECTS_DIR, exist_ok=True)

    model_config = {"env_file": ".env"}

settings = Settings()
