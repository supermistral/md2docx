from celery import Celery

from .config import settings


def create_app() -> Celery:
    app = Celery(__name__)
    app.config_from_object(settings, namespace='CELERY')
    app.conf.update(task_track_started=True)

    return app
