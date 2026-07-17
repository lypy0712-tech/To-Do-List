from pathlib import Path

from pydantic import computed_field
from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI TO-DO-List"
    DEBUG: bool = False

    DB_HOST: str
    DB_PORT: str = 15432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    CORS_ALLOWED_ORIGINS: list[str]

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = SettingsConfigDict(
        env_file=ENV_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True
    )

settings = Settings()