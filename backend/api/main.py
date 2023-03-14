import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .celery import create_app as create_celery_app
from .exceptions import BaseException, base_exception_handler
from .md2docx.router import router as md2docx_router
from .users.router import router as users_router
from .session.middleware import SessionMiddleware


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

    router = APIRouter(prefix='/api')
    router.include_router(md2docx_router)
    router.include_router(users_router)

    app.include_router(router)

    app.add_exception_handler(BaseException, base_exception_handler)

    # Run actions on app startup
    startup_actions()

    return app


app = create_app()
celery_app = create_celery_app()


if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.HOST_PORT, reload=True)
