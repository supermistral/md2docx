from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi_jwt_auth.exceptions import AuthJWTException


async def base_auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": "AuthError",
            "message": exc.message,
            "details": {"code": exc.__class__.__name__},
        },
    )
