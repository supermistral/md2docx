import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .config import settings
from .celery import create_app as create_celery_app
from .exceptions import (
    BaseException,
    NoResultFound,
    base_exception_handler,
    db_exception_handler,
    data_validation_exception_handler,
)
from .documents.router import router as documents_router
from .users.router import router as users_router
from .operations.router import router as operations_router
from .access.router import router as access_router
from .session.middleware import SessionMiddleware
from .access.exception_handlers import (
    base_auth_jwt_exception_handler,
    AuthJWTException,
)


def startup_actions() -> None:
    settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        max_age=settings.SESSION_MAX_AGE,
        session_cookie=settings.SESSION_COOKIE
    )

    router = APIRouter(prefix='/api/v1')
    router.include_router(documents_router)
    router.include_router(users_router)
    router.include_router(operations_router)
    router.include_router(access_router)

    app.include_router(router)

    app.add_exception_handler(BaseException, base_exception_handler)
    app.add_exception_handler(AuthJWTException, base_auth_jwt_exception_handler)
    app.add_exception_handler(NoResultFound, db_exception_handler)
    app.add_exception_handler(RequestValidationError, data_validation_exception_handler)

    # Run actions on app startup
    startup_actions()

    return app


app = create_app()
celery_app = create_celery_app()


if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.HOST_PORT, reload=True)
