from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
from pydantic import computed_field


class Settings(BaseSettings):
    app_name: str = "PureFile"
    debug: bool = True

    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()