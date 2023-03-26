import os
import uuid
import shutil

import pytest
from celery.result import AsyncResult

from .utils import extract_session_cookie


@pytest.fixture
def markdown_data(settings):
    yield {
        'code': 'Some markdown text'
    }

    shutil.rmtree(settings.SESSION_ROOT, ignore_errors=True)


@pytest.fixture(autouse=True)
def disable_celery(mocker):
    mocker.patch('celery.app.task.Task.apply_async', return_value=1)


def test_get_with_empty_session(client):
    response = client.get('/api/md2docx/')

    assert response.status_code == 400
    assert 'detail' in response.json()

    detail = response.json()['detail']

    assert 'session' in detail.lower()
    assert 'incorrect' in detail.lower()


def test_get_with_incorrect_session(client_with_incorrect_session):
    response = client_with_incorrect_session.get('/api/md2docx/')

    assert response.status_code == 400
    assert 'detail' in response.json()

    detail = response.json()['detail']

    assert 'session' in detail.lower()
    assert 'incorrect' in detail.lower()


def test_post_process_with_session(client_with_session, settings, markdown_data):
    response = client_with_session.post(
        '/api/md2docx/',
        data=markdown_data
    )

    assert response.status_code == 200
    assert 'session' in response.headers['Set-Cookie']

    data = extract_session_cookie(response.headers['Set-Cookie'])
    uid = data['session']['id']
    markdown_file = settings.SESSION_ROOT / uid / 'md.md'

    assert os.path.exists(markdown_file)
    assert os.path.isfile(markdown_file)

    with open(markdown_file) as f:
        content = f.read()

    assert content == markdown_data['code']


def test_post_process_with_unset_session(client, settings, markdown_data):
    response = client.post(
        '/api/md2docx/',
        data=markdown_data
    )

    assert response.status_code == 200
    assert 'session' in response.headers['Set-Cookie']

    data = extract_session_cookie(response.headers['Set-Cookie'])
    uid = data['session']['id']
    markdown_file = settings.SESSION_ROOT / uid / 'md.md'

    assert str(uuid.UUID(uid)) == uid
    assert os.path.exists(markdown_file)
    assert os.path.isfile(markdown_file)

    with open(markdown_file) as f:
        content = f.read()

    assert content == markdown_data['code']


def test_get_pending_task(client_with_session, mocker):
    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'PENDING'}
    )

    response = client_with_session.get('/api/md2docx/')

    assert response.status_code == 200
    assert response.json() == {'status': 'PENDING'}


def test_get_failure_task_with_unknown_error(client_with_session, mocker):
    error_msg = "test error msg"

    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'FAILURE', 'result': Exception(error_msg)}
    )

    response = client_with_session.get('/api/md2docx/')

    assert response.status_code == 200

    body = response.json()

    assert all(key in body for key in ['status', 'error', 'detail']) and len(body) == 3
    assert body['status'] == 'FAILURE'
    assert 'unknown' in body['error'].lower()
    assert 'unknown' in body['detail'].lower()


def test_get_failure_task(client_with_session, mocker):
    error_msg = 'test_error: [{"key": "value", "msg": "error message"}]\n'

    task = mocker.patch.object(
        AsyncResult,
        '_get_task_meta',
        side_effect=lambda: {'status': 'FAILURE', 'result': Exception(error_msg)}
    )

    response = client_with_session.get('/api/md2docx/')

    assert response.status_code == 200

    body = response.json()

    assert all(key in body for key in ['status', 'error', 'detail']) and len(body) == 3
    assert body['status'] == 'FAILURE'
    assert body['error'] == "test_error"
    assert body['detail'] == [{'key': 'value', 'msg': 'error message'}]


# TODO: get_document endpoint tests
