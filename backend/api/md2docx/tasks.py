from celery import shared_task

from md2docx import run_post_processing, run_win_processing, run_processing
from .utils import get_markdown_file_path, get_docx_file_path


@shared_task()
def process_md2docx(id: str):
    file_path = get_markdown_file_path(id)
    out_file_path = get_docx_file_path(id)

    run_processing(file_path, out_file_path)

    # win_task_id = get_task_id(id, TaskType.WIN_PROCESSING)
    # win_process_md2word.apply_async((id,), task_id=win_task_id)


@shared_task()
def win_process_md2docx(id: str):
    file_path = get_docx_file_path(id)

    run_win_processing(file_path)

    # post_task_id = get_task_id(id, TaskType.POST_PROCESSING)
    # post_process_md2word.apply_async((id,), task_id=post_task_id)


@shared_task()
def post_process_md2docx(id: str):
    file_path = get_docx_file_path(id)

    run_post_processing(file_path)
