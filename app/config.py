import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    api_title: str = os.getenv("API_TITLE", "PredictiveGuard")
    api_version: str = os.getenv("API_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    workers: int = int(os.getenv("WORKERS", "4"))

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/predictive_guard"
    )
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "predictive_guard")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")

    # Redis & Celery
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Storage
    storage_type: str = os.getenv("STORAGE_TYPE", "local")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "predictive-guard")
    upload_folder: str = os.getenv("UPLOAD_FOLDER", "./data/uploads")

    # Monitoring
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN", None)
    prometheus_port: int = int(os.getenv("PROMETHEUS_PORT", "8001"))

    # ML Models
    model_registry_path: str = os.getenv("MODEL_REGISTRY_PATH", "./models/registry")
    artifact_storage_path: str = os.getenv("ARTIFACT_STORAGE_PATH", "./models/artifacts")
    metrics_storage_path: str = os.getenv("METRICS_STORAGE_PATH", "./models/metrics")

    # Alerts
    webhook_timeout: int = int(os.getenv("WEBHOOK_TIMEOUT", "30"))
    alert_check_interval: int = int(os.getenv("ALERT_CHECK_INTERVAL", "300"))

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "dev", "development"}:
                return True
            if normalized in {"0", "false", "no", "off", "prod", "production", "release"}:
                return False
        return value

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
