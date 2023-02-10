from celery import shared_task

from md2docx import run_post_processing, run_win_processing, run_processing


@shared_task()
def process_md2docx(md_file: str, docx_file: str):
    run_processing(md_file, docx_file)


@shared_task()
def win_process_md2docx(docx_file: str):
    run_win_processing(docx_file)


@shared_task()
def post_process_md2docx(docx_file: str):
    run_post_processing(docx_file)
