import shutil

import pytest
from fastapi.testclient import TestClient

from ..main import create_app
from ..config import settings as api_settings


@pytest.fixture(scope='module')
def app_without_middlewares():
    app = create_app()

    app.user_middleware.clear()
    app.middleware_stack = app.build_middleware_stack()

    return app


@pytest.fixture(scope='module')
def client(settings):
    with TestClient(create_app()) as c:
        yield c

    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


@pytest.fixture(scope='session')
def settings():
    return api_settings


@pytest.fixture
def anyio_backend():
    return 'asyncio'
