from typing import Any

from fastapi import APIRouter, Request, Depends
from fastapi.exceptions import HTTPException

from .schemas import Markdown, Task
from .utils import get_task_result
from .service import get_md2docx_service, Md2DocxService


router = APIRouter(prefix='/md2word', tags=['md2word'])


@router.post('/')
async def post_process_md2docx(
    request: Request,
    md: Markdown,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    service.save_markdown(session_id, md.code)
    service.run_processing_tasks(session_id)

    return None


@router.get('/')
async def get_task_response(request: Request) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    task = get_task_result(session_id)

    return Task(status=task.state)
