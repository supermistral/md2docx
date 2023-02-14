from typing import Any, Union

from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.exceptions import HTTPException

from .schemas import Markdown, Task
from .utils import get_task_result
from .service import get_md2docx_service, Md2DocxService


router = APIRouter(prefix='/md2docx', tags=['md2docx'])


@router.post('/')
async def post_process_md2docx(
    request: Request,
    md: Markdown,
    images: Union[list[UploadFile], None] = None,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    service.save_markdown(session_id, md.code)

    if images is not None:
        service.save_images(session_id, images, md.images_names)

    service.run_processing_tasks(session_id)

    return None


@router.get('/')
async def get_task_response(request: Request) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    task = get_task_result(session_id)

    return Task(status=task.state)
