import asyncio

from celery import shared_task

from md2docx import run_post_processing, run_win_processing, run_processing

from .service import get_md2docx_service
from .callbacks import done_failed_processing


@shared_task(on_failure=done_failed_processing)
def process_md2docx(operation_id: str, user_id: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _process_md2docx(
            operation_id=operation_id,
            user_id=user_id,
        )
    )


@shared_task()
def win_process_md2docx(docx_file: str):
    run_win_processing(docx_file)


@shared_task()
def post_process_md2docx(docx_file: str):
    run_post_processing(docx_file)


async def _process_md2docx(operation_id: str, user_id: str):
    async for service in get_md2docx_service():
        md_file = await service.get_markdown_file_path_from_operation(
            operation_id=operation_id,
        )
        docx_file = service.get_docx_filename(
            operation_id=operation_id,
        )

        run_processing(md_file, docx_file)

        await service.done_processing(
            operation_id=operation_id,
            docx_filename=docx_file,
            user_id=user_id,
        )
