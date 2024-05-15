import uuid, json, logging
from pathlib import Path
from typing import Generator, Optional

from starlette.responses import ContentStream
from fastapi import UploadFile
from sqlalchemy import select, update

from .schemas import TaskError
from .utils import (
    save_file,
    search_serialized_error,
)
from ..config import settings
from ..object_storage.service import ObjectStorageService
from ..documents.models import DocumentRevision
from ..operations.models import Operation, OperationStatus
from ..operations.schemas import OperationCreate
from ..db.session import get_session
from ..db.service import BaseDBService

LOG = logging.getLogger(__name__)


class Md2DocxService(BaseDBService):
    """
    Performs markdown-to-docx conversion-related operations.
    """

    async def run_markdown_to_docx_conversion(
        self,
        *,
        markdown_code: str,
        user_id: str,
        images: Optional[list[UploadFile]] = None,
        images_names: Optional[list[Optional[str]]] = None,
    ):
        LOG.info("[md2docx] Started processing for user %s", user_id)

        images_names = self._get_images_names(
            images=images,
            images_names=images_names,
        )
        operation = await self._create_operation(
            user_id=user_id,
        )
        storage_images_paths = await self._create_media_files(
            images=images,
            user_id=user_id,
            images_names=images_names,
        )
        document_revision = await self._create_document_revision(
            content=markdown_code,
            operation_id=operation.id,
            storage_images_paths=storage_images_paths,
        )

        await self._run_processing_tasks(
            user_id=user_id,
            operation_id=operation.id,
        )

        await self.db.commit()

        LOG.info("[md2docx] Created operation %s for user %s", operation.id, user_id)

        return operation

    async def save_files_locally(
        self,
        *,
        operation_id: uuid.UUID,
        directory: Path,
    ) -> str:
        document_revision = await self._get_document_revision(
            operation_id=operation_id,
        )

        markdown_file_path = self._save_markdown_code_locally_from_document_revision(
            directory=directory,
            document_revision=document_revision,
        )
        self._save_media_files_locally_from_document_revision(
            directory=directory,
            document_revision=document_revision,
        )

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
        operation_id: uuid.UUID,
    ) -> str:
        return f"{str(operation_id)}.docx"

    async def done_processing(
        self,
        *,
        user_id: str,
        operation_id: uuid.UUID,
        docx_filename: str,
        docx_file_path: Path,
    ):
        object_storage_service = self._get_object_storage_service()

        storage_docx_filename = self._build_object_storage_filename(
            user_id=user_id,
            filename=docx_filename,
        )

        object_storage_service.upload_object(
            key=storage_docx_filename,
            body=docx_file_path,
            is_file=True,
        )

        response = {"docx_file": storage_docx_filename}

        await self.db.execute(
            update(Operation)
            .where(Operation.id == operation_id)
            .values(
                status=OperationStatus.SUCCECSS,
                response=response,
            )
        )
        await self.db.commit()

        LOG.info("[md2docx] Saved operation %s with response %s", operation_id, response)

    async def done_failed_processing(
        self,
        *,
        exc: Exception,
        operation_id: uuid.UUID,
    ):
        task_error = self.build_error_message(
            exc=exc,
            status=OperationStatus.FAILED,
        )
        error = task_error.model_dump(mode="json")

        await self.db.execute(
            update(Operation)
            .where(Operation.id == operation_id)
            .values(
                status=OperationStatus.FAILED,
                error=error,
            )
        )
        await self.db.commit()

    def get_document(
        self,
        *,
        name: str,
    ) -> ContentStream:
        object_storage_service = self._get_object_storage_service()
        body = object_storage_service.get_object(key=name)
        return body.iter_chunks()

    async def _create_document_revision(
        self,
        *,
        operation_id: uuid.UUID,
        content: str,
        storage_images_paths: Optional[list[str]] = None
    ) -> DocumentRevision:
        model = DocumentRevision(
            content=content,
            operation_id=operation_id,
            storage_images_paths=json.dumps(storage_images_paths),
        )
        self.db.add(model)

        await self.db.flush()

        return model

    async def _create_operation(
        self,
        *,
        user_id: str,
    ) -> Operation:
        schema = OperationCreate(created_by=user_id)
        model = Operation(**schema.model_dump())
        self.db.add(model)

        await self.db.flush()

        return model

    async def _create_media_files(
        self,
        *,
        images: Optional[list[UploadFile]],
        images_names: Optional[list[str]],
        user_id: str,
    ) -> Optional[list[str]]:
        if images is None:
            return None

        assert images_names is not None, "Logical error: images names should be set"

        object_storage_service = self._get_object_storage_service()
        paths: list[str] = []

        for image, name in zip(images, images_names):
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

            paths.append(filename)

        return paths

    async def _run_processing_tasks(
        self,
        *,
        user_id: str,
        operation_id: uuid.UUID,
    ) -> None:
        from .tasks import process_md2docx

        str_operation_id = str(operation_id)

        process_md2docx.apply_async(
            kwargs={
                "operation_id": operation_id,
                "user_id": user_id,
            },
            task_id=str_operation_id,
        )

    async def _get_document_revision(
        self,
        *,
        operation_id: uuid.UUID,
    ) -> DocumentRevision:
        model = await self.db.execute(
            select(DocumentRevision)
            .join_from(Operation, DocumentRevision)
            .where(Operation.id == operation_id)
        )
        return model.scalar_one()

    def _get_images_names(
        self,
        *,
        images: Optional[list[UploadFile]],
        images_names: Optional[list[Optional[str]]],
    ):
        if images is None:
            return None

        if images_names is None:
            names = [file.filename for file in images]
        else:
            # TODO: Validate lengths (images and images_names)
            names = [(images_names[i] or images[i].filename) for i in range(len(images))]

        return names

    def _save_markdown_code_locally_from_document_revision(
        self,
        *,
        directory: Path,
        document_revision: DocumentRevision,
    ) -> Path:
        markdown_code = document_revision.content
        markdown_file_path = directory / f"markdown.md"

        save_file(markdown_file_path, markdown_code)

        return markdown_file_path

    def _save_media_files_locally_from_document_revision(
        self,
        *,
        directory: Path,
        document_revision: DocumentRevision,
    ) -> Optional[list[str]]:
        storage_paths = json.loads(document_revision.storage_images_paths)

        if storage_paths is None:
            return None

        names = [Path(path).name for path in storage_paths]

        object_storage_service = self._get_object_storage_service()
        paths: list[str] = []

        for name, storage_path in zip(names, storage_paths):
            body = object_storage_service.get_object(key=storage_path)
            image = body.read().decode("utf-8")
            local_path = directory / name

            save_file(local_path, image)

            paths.append(local_path)

        return paths

    def _build_object_storage_filename(
        self,
        *,
        user_id: str,
        filename: str,
    ) -> str:
        return f"{user_id}/{filename}"

    def build_error_message(self, exc: Exception, status: str) -> TaskError:
        result = search_serialized_error(str(exc))

        if result is None:
            return TaskError(
                error="UnknownError",
                details="Unknown error",
                status=status,
            )

        error, details = result
        return TaskError(
            error=error,
            details=details,
            status=status,
        )

    def _get_object_storage_service(self) -> ObjectStorageService:
        return ObjectStorageService(
            default_bucket=settings.OBJECT_STORAGE_USERS_BUCKET,
        )


async def get_md2docx_service() -> Generator[Md2DocxService, None, None]:
    async with get_session() as session:
        yield Md2DocxService(session)
