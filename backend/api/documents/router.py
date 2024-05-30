from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.responses import StreamingResponse
from celery import states as celery_states

from .service import DocumentsService, get_documents_service
from .schemas import ListDocumentTemplatesResponse
from ..md2docx.schemas import MarkdownForm, Task
from ..md2docx.utils import get_task_result
from ..md2docx.service import get_md2docx_service, Md2DocxService
from ..md2docx.dependencies import verify_session
from ..operations import schemas as operations_schemas
from ..users.utils import generate_created_by


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(verify_session)]
)


@router.post("/", response_model=operations_schemas.OperationResponse)
async def process_md2docx(
    request: Request,
    md: MarkdownForm = Depends(),
    images: Optional[list[UploadFile]] = None,
    service: Md2DocxService = Depends(get_md2docx_service),
    # user_id: str = Depends(generate_created_by),
) -> Any:
    user_id = generate_created_by(request)

    operation = await service.run_markdown_to_docx_conversion(
        markdown_code=md.code,
        user_id=user_id,
        images=images,
        images_names=md.images_names,
    )

    return operation


# DEPRECATED
@router.get("/")
async def get_task_response(
    request: Request,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    session_id = request.session.get('id')
    task = get_task_result(session_id)

    if task.state == celery_states.FAILURE:
        return service.build_error_message(exc=task.result, status=task.state)

    return Task(status=task.state)


@router.get("/files")
async def get_document(
    name: str,
    service: Md2DocxService = Depends(get_md2docx_service),
) -> Any:
    chunks = service.get_document(
        name=name,
    )
    filename = Path(name).name

    return StreamingResponse(
        content=chunks,
        headers={"Content-Disposition": f"attachment;filename={filename}"},
    )


@router.get("/templates", response_model=ListDocumentTemplatesResponse)
async def get_document_templates(
    service: DocumentsService = Depends(get_documents_service),
):
    templates = await service.get_all_document_templates()

    return ListDocumentTemplatesResponse(
        templates=templates,
    )
