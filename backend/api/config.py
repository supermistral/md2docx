import os
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, RedisDsn, AmqpDsn
from celery.schedules import crontab


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Markdown-to-word app"
    PROJECT_DESCRIPTION: str = "App allowing translate Markdown code to Word file .docx"
    PROJECT_VERSION: str = "1.0"
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    HOST_HTTP: str = os.environ.get('HOST_HTTP', 'http://')
    HOST_URL: str = os.environ.get('HOST_URL', 'localhost')
    HOST_PORT: int = int(os.environ.get('HOST_PORT', 8000))
    BASE_URL: str = f'{HOST_HTTP}{HOST_URL}:{HOST_PORT}'
    ALLOWED_ORIGINS: list[str] = os.environ.get('ALLOWED_ORIGINS', '*').split()

    CELERY_broker_url: AmqpDsn = os.environ.get('CELERY_BROKER_URL')
    CELERY_result_backend: RedisDsn = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_timezone: str = os.environ.get('TZ', 'Europe/London')
    CELERY_IMPORTS: list[str] = ['api.md2docx.tasks', 'api.session.tasks']
    CELERY_BEAT_SCHEDULE: dict[str, dict[str, Any]] = {
        'check_and_delete_sessions': {
            'task': 'api.session.tasks.delete_wrong_sessions',
            'schedule': crontab(),
        }
    }

    SESSION_BACKEND_URL: str = os.environ.get('SESSION_BACKEND_URL')
    SESSION_COOKIE: str = 'session'
    SESSION_MAX_AGE: Optional[int] = os.environ.get('SESSION_MAX_AGE', 20)

    BASE_DIR: Path = Path(__file__).resolve().parent

    MEDIA_URL: str = 'media'
    MEDIA_ROOT: Path = BASE_DIR / MEDIA_URL
    SESSION_ROOT: Path = MEDIA_ROOT / 'md2docx' / 'session'


class DevelopmentSettings(Settings):
    pass


class ProductionSettings(Settings):
    CELERY_BEAT_SCHEDULE: dict[str, dict[str, Any]] = {
        'check_and_delete_sessions': {
            'task': 'api.session.tasks.delete_wrong_sessions',
            'schedule': crontab(minute=0, hour=0),
        }
    }


def get_settings() -> Settings:
    if os.environ.get('ENVIRONMENT', 'development').lower() == 'production':
        settings = ProductionSettings()
    else:
        settings = DevelopmentSettings()

    return settings


settings = get_settings()
