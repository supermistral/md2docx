import uuid

import pytest

from ...session.storage import SessionStorage


@pytest.fixture
def item():
    return {
        'key': 'test_key',
        'value': 'test_value'
    }


@pytest.fixture
async def storage(item):
    storage = SessionStorage()
    await storage.client.set(item['key'], item['value'])
    yield storage
    await storage.client.delete(item['key'])


@pytest.mark.anyio
async def test_session_exists(storage, item):
    test_key_exists = await storage.session_exists(item['key'])
    empty_key_exists = await storage.session_exists('empty_key')

    assert test_key_exists == True
    assert empty_key_exists == False


@pytest.mark.anyio
async def test_generate_session_id(storage, item):
    id = await storage.generate_session_id()
    
    assert id != item['key']

    id_in_session = await storage.client.get(id)
    uid = uuid.UUID(id)

    assert str(uid) == id
    assert id_in_session is None


@pytest.mark.anyio
async def test_add_session(storage):
    key, value = 'second_test_key', 'second_test_value'
    await storage.add_session(key, value)
    result = await storage.client.get(key)

    assert result == value


@pytest.mark.anyio
async def test_get_session(storage, item):
    result = await storage.get_session(item['key'])

    assert result == item['value']


@pytest.mark.anyio
async def test_del_session(storage, item):
    await storage.del_session(item['key'])
    result = await storage.client.get(item['key'])

    assert result is None
