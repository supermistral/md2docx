import pytest

from .utils import create_session_cookie


@pytest.fixture(scope='module')
def session_data():
    return {'id': 'test_id'}


@pytest.fixture(scope='module')
def cookie_session_data(session_data):
    return {'session': session_data}


@pytest.fixture(scope='module')
def client_with_session(client, session_data):
    client.cookies = {'session': create_session_cookie(session_data)}
    return client


@pytest.fixture(scope='module')
def client_with_incorrect_session(client):
    client.cookies = {'session': 'incorrect_session'}
    return client
