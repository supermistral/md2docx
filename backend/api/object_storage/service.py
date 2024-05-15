from typing import Any, Optional

import boto3

from .decorators import with_error_wrapper
from .session import SESSION
from ..config import settings


class ObjectStorageService:
    def __init__(
        self,
        *,
        endpoint_url: str = settings.OBJECT_STORAGE_ENDPOINT_URL,
        default_bucket: Optional[str] = None,
    ) -> None:
        self.client = self.__create_client(
            session=SESSION,
            endpoint_url=endpoint_url,
        )
        self.default_bucket = default_bucket

    @with_error_wrapper
    def upload_object(
        self,
        *,
        key: str,
        body: Any,
        is_file: bool = False,
        is_binary: bool = False,
        bucket: Optional[str] = None,
        storage_class: Optional[str] = None,
    ):
        bucket = bucket or self.default_bucket

        if is_file:
            if is_binary:
                return self.client.upload_fileobj(body, bucket, key)

            return self.client.upload_file(body, bucket, key)            

        kwargs = {}

        if storage_class is not None:
            kwargs["StorageClass"] = storage_class

        return self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            **kwargs,
        )

    @with_error_wrapper
    def get_object(
        self,
        key: str,
        *,
        bucket: Optional[str] = None,
    ):
        bucket = bucket or self.default_bucket
        response = self.client.get_object(
            Bucket=bucket,
            Key=key,
        )
        return response["Body"]

    def __create_client(
        self,
        *,
        session: boto3.Session,
        endpoint_url: str,
        service_name: str = "s3",
    ):
        return session.client(
            service_name=service_name,
            endpoint_url=endpoint_url,
        )
