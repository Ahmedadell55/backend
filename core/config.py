import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impnb2l6b2ZveWdvZXd0ZHJ4YXR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzAwNjAwNywiZXhwIjoyMDkyNTgyMDA3fQ.8_pIw5RWLfNJoSXDEzWJtmQitj76gBaA5ywZ0SfgzhE"
    SUPABASE_URL: str = "https://jgoizofoygoewtdrxatx.supabase.co"
    PROJECTS_DIR: str = "saved_projects"
    APP_NAME: str = "Darb SmartCity API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    # ⬇️ هتحطه في Railway Variables بعد ما تاخد رابط Netlify
    FRONTEND_URL: str = "https://taupe-pika-a4c3de.netlify.app"

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


settings = Settings()
