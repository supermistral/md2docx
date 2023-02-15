import shutil
import os

from celery import shared_task

from .storage import session_storage
from ..config import settings


@shared_task(autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 10, 'countdown': 10})
def delete_wrong_sessions():
    for dir in os.listdir(settings.SESSION_ROOT):
        if os.path.isdir(settings.SESSION_ROOT / dir):
            delete_session.delay(dir)


@shared_task(autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 5, 'countdown': 10})
def delete_session(dir: str):
    session_storage.del_session(dir)
    shutil.rmtree(settings.SESSION_ROOT / dir)
