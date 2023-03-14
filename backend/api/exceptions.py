from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class BaseException(HTTPException):
    """
    Unified interface for handling custom errors
    """

    def __init__(self, status_code: int, detail: Any, error_type: str, **kwargs) -> None:
        super().__init__(status_code, detail, **kwargs)
        self.error_type = error_type


async def base_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.error_type, 'detail': exc.detail}
    )
