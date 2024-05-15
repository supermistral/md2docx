import asyncio, tempfile
from pathlib import Path

from celery import shared_task

from md2docx import (
    run_post_processing,
    run_win_processing,
    run_processing,
)

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


async def _process_md2docx(operation_id: str, user_id: str):
    directory = tempfile.TemporaryDirectory(prefix=f"{operation_id}_")
    directory_path = Path(directory.name)

    # 1. Update status for operation
    async for service in get_md2docx_service():
        md_file_path = await service.save_files_locally(
            operation_id=operation_id,
            directory=directory_path,
        )

    # 2. Execute processing
    async for service in get_md2docx_service():
        docx_filename = service.get_docx_filename(
            operation_id=operation_id,
        )
        docx_file_path = directory_path / docx_filename

        run_processing(
            md_file_path,
            docx_file_path,
            media_dir=directory_path,
        )
        # run_post_processing(md_file_path)

        await service.done_processing(
            operation_id=operation_id,
            docx_filename=docx_filename,
            docx_file_path=docx_file_path,
            user_id=user_id,
        )

    directory.cleanup()
