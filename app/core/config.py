# from pydantic_settings import BaseSettings
# import os


# class Settings(BaseSettings):
#     DATABASE_URL: str = "sqlite:///./tasks.db"

#     SECRET_KEY: str = os.getenv(
#         "SECRET_KEY"
#     )

#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

#     CELERY_BROKER_URL: str = os.getenv(
#         "CELERY_BROKER_URL",
#         "redis://localhost:6379/0"
#     )

#     CELERY_RESULT_BACKEND: str = os.getenv(
#         "CELERY_RESULT_BACKEND",
#         "redis://localhost:6379/0"
#     )

#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./tasks.db"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment Settings
    DEBUG: bool = False

    # Celery Settings
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()