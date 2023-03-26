import os
import shutil
import uuid
from io import BytesIO

import pytest
from fastapi import UploadFile

from ...md2docx.service import Md2DocxService


@pytest.fixture(scope='session')
def service():
    return Md2DocxService()


@pytest.fixture
def markdown_data():
    return {
        'id': str(uuid.uuid4()),
        'content': 'test markdown code'
    }


@pytest.fixture
def images():
    images_data = [
        ['1.png', "image content 1", None],
        ['2.png', "image content 2", None],
        ['3.png', "image content 3", None],
    ]

    for image_item in images_data:
        name, content = image_item[:2]

        temp_file = BytesIO(content.encode('utf-8'))
        image = UploadFile(filename=name, file=temp_file)
        image_item[2] = image

    return images_data


@pytest.fixture
def dir_path(settings, markdown_data):
    yield settings.SESSION_ROOT / markdown_data['id']
    shutil.rmtree(dir_path, ignore_errors=True)


@pytest.fixture
def created_dir_path(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)


def test_save_markdown(service, markdown_data, dir_path):
    service.save_markdown(markdown_data['id'], markdown_data['content'])
    path = dir_path / 'md.md'

    assert os.path.exists(path)
    assert os.path.isfile(path)

    with open(path) as f:
        content = f.read()

    assert content == markdown_data['content']


def test_save_images(service, markdown_data, images, created_dir_path):
    service.save_images(markdown_data['id'], images=[img[-1] for img in images])

    expected_paths = [created_dir_path / name for name, *_ in images]

    for i in range(len(images)):
        path, content = expected_paths[i], images[i][1]
        assert os.path.exists(path)
        assert os.path.isfile(path)

        with open(path) as f:
            real_content = f.read()

        assert real_content == content


def test_save_images_with_names(service, markdown_data, images, created_dir_path):
    images_names = ['4.png', '5.png', '6.png']

    service.save_images(
        markdown_data['id'],
        images=[img[-1] for img in images],
        images_names=images_names
    )

    expected_paths = [created_dir_path / name for name in images_names]

    for i in range(len(images)):
        path, content = expected_paths[i], images[i][1]

        assert os.path.exists(path)
        assert os.path.isfile(path)

        with open(path) as f:
            real_content = f.read()

        assert real_content == content


def test_save_images_with_partial_names(service, markdown_data, images, created_dir_path):
    images_names = [None, '7.png', None]
    expected_names = ['1.png', '7.png', '3.png']

    service.save_images(
        markdown_data['id'],
        images=[img[-1] for img in images],
        images_names=images_names
    )

    expected_paths = [created_dir_path / name for name in expected_names]

    for i in range(len(images)):
        path, content = expected_paths[i], images[i][1]

        assert os.path.exists(path)
        assert os.path.isfile(path)

        with open(path) as f:
            real_content = f.read()

        assert real_content == content


def test_get_non_existent_docx_file(service, markdown_data, dir_path):
    path = dir_path / 'docx.docx'

    docx = service.get_docx_file(markdown_data['id'])

    assert docx is None
    assert os.path.exists(path) == False


def test_get_existent_docx_file(service, markdown_data, created_dir_path):
    path = created_dir_path / 'docx.docx'
    content = b"test docx content"
    dir_files_names = os.listdir(created_dir_path)

    with open(path, 'wb') as f:
        f.write(content)

    docx = service.get_docx_file(markdown_data['id'])

    assert docx is not None

    real_path, real_name = docx

    assert real_path == str(path)
    assert real_name not in dir_files_names


def test_get_non_existent_document(service, markdown_data, dir_path):
    path = dir_path / 'docx.docx'

    docx = service.get_document(markdown_data['id'], 'docx')

    assert docx is None
    assert os.path.exists(path) == False


def test_get_existent_document(service, markdown_data, created_dir_path):
    path = created_dir_path / 'docx.docx'
    content = b"test docx content"

    with open(path, 'wb') as f:
        f.write(content)

    docx = service.get_document(markdown_data['id'], 'docx')

    assert docx is not None

    real_path, real_name = docx
    uid_ext = uuid.UUID(markdown_data['id']).hex + '.docx'

    assert real_path == str(path)
    assert real_name == uid_ext


def test_build_error_message_by_incorrect_traceback(service, mocker):
    mocker.patch('api.md2docx.service.search_serialized_error', return_value=None)

    error_msg = "test error msg"
    error_status = 'FAILURE'
    exception = Exception(error_msg)

    msg = service.build_error_message(exception, status=error_status)

    assert msg is not None
    assert msg.status == error_status
    assert 'unknown' in msg.error.lower()
    assert isinstance(msg.detail, str)


def test_build_error_message_by_correct_traceback(service, mocker):
    error_type = 'test_key'
    error_msg = "test error msg"
    error_status = 'FAILURE'
    exception = Exception(error_msg)

    search = mocker.patch('api.md2docx.service.search_serialized_error')
    search.return_value = (error_type, error_msg)

    msg = service.build_error_message(exception, status=error_status)

    assert msg is not None
    assert msg.status == error_status
    assert msg.error == error_type
    assert msg.detail == error_msg
