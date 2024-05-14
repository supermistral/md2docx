import logging
from typing import Any, Literal, Optional

from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from fastapi.responses import FileResponse
from celery import states as celery_states

from ..md2docx.schemas import MarkdownForm, Task
from ..md2docx.utils import get_task_result
from ..md2docx.service import get_md2docx_service, Md2DocxService
from ..md2docx.dependencies import verify_session
from ..operations import schemas as operations_schemas
from ..users.utils import generate_created_by


router = APIRouter(
    prefix='/documents',
    tags=['documents'],
    dependencies=[Depends(verify_session)]
)


@router.post('/', response_model=operations_schemas.OperationResponse)
async def process_md2docx(
    md: MarkdownForm = Depends(),
    images: Optional[list[UploadFile]] = None,
    service: Md2DocxService = Depends(get_md2docx_service),
    user_id: str = Depends(generate_created_by),
) -> Any:
    operation = await service.run_markdown_to_docx_conversion(
        markdown_code=md.code,
        user_id=user_id,
        images=images,
        images_names=md.images_names,
    )

    return operation


@router.get('/')
async def get_task_response(
    request: Request,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')
    task = get_task_result(session_id)

    if task.state == celery_states.FAILURE:
        return service.build_error_message(exc=task.result, status=task.state)

    return Task(status=task.state)


@router.get('/{doc_format}')
async def get_document(
    doc_format: Literal['docx', 'pdf'],
    request: Request,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')
    file = service.get_document(session_id, doc_format=doc_format)

    if file is None:
        raise HTTPException(404)

    path, name = file
    return FileResponse(
        path,
        filename=name,
        media_type='application/octet-stream',
    )
