from typing import Any, Optional

from pydantic import ValidationError
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import NoResultFound


class BaseException(HTTPException):
    """
    Unified interface for handling custom errors
    """

    STATUS: int = ...
    CODE: str = ...
    MESSAGE: str = ...

    def __init__(
        self,
        status_code: Optional[int] = None,
        message: Optional[str] = None,
        details: Any = None,
        code: Optional[str] = None,
        **kwargs,
    ) -> None:
        status_code = status_code or self.STATUS

        super().__init__(status_code, details)

        self.code = code or self.CODE
        self.message = (message or self.MESSAGE).format(**kwargs)
        self.details = details


async def base_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        }
    )


class NotFoundException(BaseException):
    STATUS = 404
    CODE = "NotFound"
    MESSAGE = "Resource not found."

    def __init__(
        self,
        filters: Optional[list[tuple[str, Any]]] = None,
        resource: Optional[str] = None,
    ) -> None:
        details = {"filters": filters, "resource": resource}
        details = {k: v for k, v in details.items() if v is not None}

        super().__init__(
            details=details,
        )


class RequestValidationException(BaseException):
    STATUS = 400
    CODE = "Validation"
    MESSAGE = "The request failed during data validation."


async def db_exception_handler(request: Request, exc: NoResultFound):
    return await base_exception_handler(
        request=request,
        exc=NotFoundException()
    )


async def data_validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()

    for error in details:
        error.pop("ctx")
        error.pop("input")
        error["message"] = error.pop("msg")

    return await base_exception_handler(
        request=request,
        exc=RequestValidationException(details=details),
    )
