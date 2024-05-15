from typing import Any, Callable

from fastapi import HTTPException
from botocore import exceptions as boto_exceptions

from ..exceptions import NotFoundException


def with_error_wrapper(f: Callable) -> Callable:
    def error_wrapper(*args, **kwargs) -> Any:
        try:
            return f(*args, **kwargs)
        except boto_exceptions.ClientError as exc:
            code = exc.response["Error"]["Code"]

            if code == "NoSuchKey":
                raise NotFoundException()

            status_code = exc.response["ResponseMetadata"]["HTTPStatusCode"]
            message = exc.response["Error"]["Message"]

            raise HTTPException(
                status_code=status_code,
                message=message,
                code=code,
            )

    return error_wrapper
