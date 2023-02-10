from pathlib import Path

from celery.result import AsyncResult

from .schemas import TaskType
from ..config import settings


TASK_ID_GENERATORS = {
    TaskType.PROCESSING: lambda s: f'processing_{s}',
    TaskType.WIN_PROCESSING: lambda s: f'win_processing_{s}',
    TaskType.POST_PROCESSING: lambda s: f'post_processing_{s}',
}


def get_task_id(id: str, task_type: TaskType) -> str:
    return TASK_ID_GENERATORS[task_type](id)


def get_task_result(id: str) -> AsyncResult:
    task = AsyncResult(id)
    return task


def get_media_dir_by_id(id: str) -> Path:
    return settings.MEDIA_ROOT / 'md2docx' / 'session' / id


def save_markdown(id: str, content: str) -> None:
    media_dir = get_media_dir_by_id(id)
    media_dir.mkdir(parents=True, exist_ok=True)

    file_path = media_dir / 'md.md'

    with open(file_path, 'w') as f:
        f.write(content)


def get_markdown_file_path(id: str) -> Path:
    return get_media_dir_by_id(id) / 'md.md'


def get_docx_file_path(id: str) -> Path:
    return get_media_dir_by_id(id) / 'docx.docx'
