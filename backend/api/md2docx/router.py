from typing import Any

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from .schemas import Markdown, Task
from .utils import get_task_result, save_markdown
from .tasks import process_md2docx, win_process_md2docx, post_process_md2docx


router = APIRouter(prefix='/md2word', tags=['md2word'])


@router.post('/')
async def post_process_md2docx(request: Request, md: Markdown) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    save_markdown(session_id, md.code)

    task = (process_md2docx.s(session_id)).apply_async(task_id=session_id)

    return None


@router.get('/')
async def get_task_response(request: Request) -> Any:
    session_id = request.session.get('id')

    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")

    task = get_task_result(session_id)
    return Task(status=task.state)
