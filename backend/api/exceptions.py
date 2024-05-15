from typing import Any, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class BaseException(HTTPException):
    """
    Unified interface for handling custom errors
    """

    CODE: str = ...

    def __init__(
        self,
        status_code: int,
        message: str,
        details: Any = None,
        code: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(status_code, details, **kwargs)
        self.code = code or self.CODE
        self.message = message
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
    CODE = "NotFound"

    def __init__(self, filters: Optional[list[tuple[str, Any]]] = None) -> None:
        super().__init__(
            status_code=404,
            message="Resource not found.",
            details=filters,
        )
