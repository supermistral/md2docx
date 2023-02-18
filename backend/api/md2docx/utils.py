import shutil
import json
import re
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Any, Optional, Union

from celery.result import AsyncResult

from .schemas import TaskType


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


def create_file_directory(path: str) -> None:
    Path(path).resolve().parent.mkdir(parents=True, exist_ok=True)


def save_file(file: Path, content: str) -> None:
    with open(file, 'w') as f:
        f.write(content)


def save_file_by_chunk(file: SpooledTemporaryFile, name: Union[Path, str]) -> None:
    with open(name, 'wb+') as f:
        shutil.copyfileobj(file, f)


def search_serialized_error(traceback: str) -> Optional[tuple[str, Any]]:
    regex = re.search(r'(\w+): (.+?)\n', traceback)

    if regex is None:
        return None

    return regex.group(1), json.loads(regex.group(2))
