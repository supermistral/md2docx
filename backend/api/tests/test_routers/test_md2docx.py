from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request
from celery.result import AsyncResult

from ...md2docx.service import Md2DocxService, get_md2docx_service


def get_app_with_overrided_service(
    mocker,
    app: FastAPI,
    methods: dict[str, Any],
    base_path: str = 'api.md2docx.service.Md2DocxService.'
) -> FastAPI:
    for method, return_value in methods.items():
        func = mocker.patch(base_path + method)
        func.return_value = return_value

    overrided_get_md2docx_service = lambda: Md2DocxService()
    app.dependency_overrides[get_md2docx_service] = overrided_get_md2docx_service
    return app


@pytest.fixture
def markdown_data():
    return {
        'code': 'Some markdown text'
    }


@pytest.fixture
def cookies():
    return {'session': 'test_id'}


@pytest.fixture(autouse=True)
def session_in_request(mocker):
    req = mocker.patch.object(Request, 'session', mocker.PropertyMock)
    req.get = lambda id: 'test_id'


def test_post_process(mocker, app_without_middlewares, markdown_data, cookies):
    app = get_app_with_overrided_service(mocker, app_without_middlewares, {
        'save_markdown': None,
        'save_images': None,
    })

    with TestClient(app) as client:
        response = client.post(
            '/api/md2docx/',
            data=markdown_data,
            cookies=cookies
        )
        assert response.status_code == 200


def test_get_pending_task(mocker, app_without_middlewares, cookies):
    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'PENDING'}
    )

    with TestClient(app_without_middlewares) as client:
        response = client.get('/api/md2docx/', cookies=cookies)

        assert response.status_code == 200
        assert response.json() == {'status': 'PENDING'}


def test_get_success_task(mocker, app_without_middlewares, cookies):
    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'SUCCESS'}
    )

    with TestClient(app_without_middlewares) as client:
        response = client.get('/api/md2docx/', cookies=cookies)

        assert response.status_code == 200
        assert response.json() == {'status': 'SUCCESS'}


@pytest.mark.parametrize('task_error', [{
    'status': "FAILURE",
    'detail': "Unknown error",
    'error': "UnknownError"
}])
def test_get_failure_task(mocker, app_without_middlewares, task_error, cookies):
    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'FAILURE', 'result': Exception()}
    )

    app = get_app_with_overrided_service(
        mocker,
        app_without_middlewares,
        methods={
            'build_error_message': task_error
        },
    )

    with TestClient(app) as client:
        response = client.get('/api/md2docx/', cookies=cookies)

        assert response.status_code == 200
        assert response.json() == task_error


def test_get_non_existent_document(mocker, app_without_middlewares, cookies):
    app = get_app_with_overrided_service(
        mocker,
        app_without_middlewares,
        methods={
            'get_document': None,
        },
    )

    with TestClient(app) as client:
        response = client.get('/api/md2docx/document/docx', cookies=cookies)

        assert response.status_code == 404


def test_get_existent_document(mocker, app_without_middlewares, cookies, tmp_path):
    filename = 'test.docx'
    path = tmp_path / filename
    content = b"file content"

    with open(path, 'wb') as f:
        f.write(content)

    disposition = 'attachment; filename="test.docx"'

    app = get_app_with_overrided_service(
        mocker,
        app_without_middlewares,
        methods={
            'get_document': (path, filename),
        },
    )

    with TestClient(app) as client:
        response = client.get('/api/md2docx/document/docx', cookies=cookies)

        assert response.status_code == 200
        assert response.content == content
        assert response.headers['content-disposition'] == disposition
        assert response.headers['content-type'] == 'application/octet-stream'


def test_get_invalid_format_document(app_without_middlewares, cookies):
    with TestClient(app_without_middlewares) as client:
        response = client.get('/api/md2docx/document/doc', cookies=cookies)

        assert response.status_code == 422
