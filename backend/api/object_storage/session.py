import boto3

from ..config import settings


SESSION = boto3.Session(
    access_key_id=settings.OBJECT_STORAGE_ACCESS_KEY_ID,
    secret_access_key=settings.OBJECT_STORAGE_SECRET_ACCESS_KEY,
    region_name=settings.OBJECT_STORAGE_REGION_NAME,
)
