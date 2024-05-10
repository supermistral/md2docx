import uuid
from pathlib import Path
from typing import Any, Generator, Literal, Optional

from fastapi import UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .tasks import process_md2docx, post_process_md2docx
from .schemas import TaskError, TaskType
from .utils import (
    save_file,
    get_task_id,
    create_file_directory,
    save_file_by_chunk,
    search_serialized_error,
)
from ..config import settings
from ..object_storage.service import ObjectStorageService
from ..documents.models import DocumentRevision
from ..operations.models import Operation, OperationStatus
from ..db.session import get_session


class Md2DocxService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def run_markdown_to_docx_conversion(
        self,
        *,
        markdown_code: str,
        user_id: str,
        images: Optional[list[UploadFile]] = None,
        images_names: Optional[list[str]] = None,
    ):
        operation = await self._create_operation(
            user_id=user_id,
        )
        document_revision = await self._create_document_revision(
            content=markdown_code,
            operation_id=operation.id,
        )

        if images is not None:
            await self._create_media_files(
                images=images,
                user_id=user_id,
                images_names=images_names,
            )

        self._run_processing_tasks(
            user_id=user_id,
            operation_id=operation.id,
        )

        await self.db.commit()

        return operation

    async def get_markdown_file_path_from_operation(
        self,
        *,
        operation_id: str,
    ) -> str:
        model = await self.db.execute(
            select(DocumentRevision)
            .join_from(Operation, DocumentRevision)
            .where(Operation.id == operation_id)
        )
        document_revision = model.scalar_one()
        markdown_code = document_revision.content
        markdown_file_path = f"{operation_id}.md"

        save_file(markdown_file_path, markdown_code)

        await self.db.execute(
            update(Operation)
            .where(Operation.id == operation_id)
            .values(status=OperationStatus.IN_PROGRESS)
        )
        await self.db.commit()

        return markdown_file_path

    def get_docx_filename(
        self,
        *,
        operation_id: str,
    ) -> str:
        return f"{operation_id}.docx"

    async def done_processing(
        self,
        *,
        user_id: str,
        operation_id: str,
        docx_filename: str,
    ):
        object_storage_service = self._get_object_storage_service()

        docx_filename = self._build_object_storage_filename(
            user_id=user_id,
            filename=docx_filename,
        )

        object_storage_service.upload_object(
            key=docx_filename,
            body=docx_filename,
            is_file=True,
        )

        response = {"docx_filename": docx_filename}

        await self.db.execute(
            update(Operation)
            .where(Operation.id == operation_id)
            .values(
                status=OperationStatus.SUCCECSS,
                response=response,
            )
        )
        await self.db.commit()

    async def done_failed_processing(
        self,
        *,
        exc: Exception,
        operation_id: str,
    ):
        task_error = self.build_error_message(
            exc=exc,
            status=OperationStatus.FAILED,
        )
        error = {**task_error}

        await self.db.execute(
            update(Operation)
            .where(Operation.id == operation_id)
            .values(
                status=OperationStatus.FAILED,
                error=error,
            )
        )
        await self.db.commit()

    async def _create_document_revision(
        self,
        *,
        operation_id: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> DocumentRevision:
        model = DocumentRevision(
            content=content,
            metadata=metadata,
            operation_id=operation_id,
        )
        self.db.add(model)

        return model

    async def _create_operation(
        self,
        *,
        user_id: str,
    ) -> Operation:
        model = Operation(
            created_by=user_id,
        )
        self.db.add(model)

        return model

    async def _create_media_files(
        self,
        *,
        images: list[UploadFile],
        user_id: str,
        images_names: Optional[list[Optional[str]]] = None,
    ):
        if images_names is None:
            names = [file.filename for file in images]
        else:
            # TODO: Validate lengths (images and images_names)
            names = [(images_names[i] or images[i].filename) for i in range(len(images))]

        object_storage_service = self._get_object_storage_service()

        for image, name in zip(images, names):
            filename = self._build_object_storage_filename(
                user_id=user_id,
                filename=name,
            )
            object_storage_service.upload_object(
                key=filename,
                body=image.file,
                is_file=True,
                is_binary=True,
            )

    def _run_processing_tasks(
        self,
        *,
        user_id: str,
        operation_id: str,
    ) -> None:
        processing_task_id = get_task_id(operation_id, TaskType.PROCESSING)
        post_processing_task_id = get_task_id(operation_id, TaskType.POST_PROCESSING)

        task = (
            process_md2docx.subtask(
                kwargs={
                    "operation_id": operation_id,
                    "user_id": user_id,
                },
                task_id=processing_task_id,
            )
            # | post_process_md2docx.subtask(
            #     (docx_filename,),
            #     task_id=post_processing_task_id,
            # )
        ).apply_async(task_id=operation_id)

    def _build_object_storage_filename(
        self,
        *,
        user_id,
        filename: str,
    ) -> str:
        return f"{user_id}/{filename}"

    def build_error_message(self, exc: Exception, status: str) -> TaskError:
        result = search_serialized_error(str(exc))

        if result is None:
            return TaskError(
                error="UnknownError",
                detail="Unknown error",
                status=status,
            )

        error, detail = result
        return TaskError(
            error=error,
            detail=detail,
            status=status,
        )

    def _get_object_storage_service(self) -> ObjectStorageService:
        return ObjectStorageService(
            default_bucket=settings.OBJECT_STORAGE_USERS_BUCKET,
        )


async def get_md2docx_service() -> Generator[Md2DocxService, None, None]:
    async with get_session() as session:
        yield Md2DocxService(session)
