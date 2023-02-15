from typing import Any, Optional

from fastapi import APIRouter, Request, Depends, UploadFile

from .schemas import MarkdownForm, Task
from .utils import get_task_result
from .service import get_md2docx_service, Md2DocxService
from .dependencies import verify_session


router = APIRouter(
    prefix='/md2docx',
    tags=['md2docx'],
    dependencies=[Depends(verify_session)]
)


@router.post('/')
async def post_process_md2docx(
    request: Request,
    md: MarkdownForm = Depends(),
    images: Optional[list[UploadFile]] = None,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')

    service.save_markdown(session_id, md.code)

    if images is not None:
        service.save_images(session_id, images, md.images_names)

    service.run_processing_tasks(session_id)

    return None


@router.get('/')
async def get_task_response(request: Request) -> Any:
    session_id = request.session.get('id')
    task = get_task_result(session_id)

    return Task(status=task.state)
