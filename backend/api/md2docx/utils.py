from pathlib import Path

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


def save_file(file: Path, content: str) -> None:
    file.resolve().parent.mkdir(parents=True, exist_ok=True)

    with open(file, 'w') as f:
        f.write(content)
