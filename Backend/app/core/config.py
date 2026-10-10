from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HelpDesk Pro"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    version: str = "1.0.0"

    database_url: str = "sqlite:///./helpdesk.db"

    jwt_secret_key: str = "dev_secret_change_me"
    access_token_minutes: int = 15
    refresh_token_days: int = 7

    frontend_origin: str = "http://localhost:5173"

    upload_dir: str = "./private_uploads"
    max_upload_size_mb: int = 5

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    email_from: str = "support@example.test"
    email_enabled: bool = False

    seed_admin_name: str = "System Administrator"
    seed_admin_email: str = "admin@example.test"
    seed_admin_password: str = "ChangeMe123!"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()