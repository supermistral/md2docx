import uuid
from pathlib import Path
from typing import Generator, Literal, Optional

from fastapi import UploadFile

from .tasks import process_md2docx, post_process_md2docx
from .schemas import TaskError, TaskType
from .utils import (
    save_file, get_task_id, save_file_by_chunk, create_file_directory,
    search_serialized_error
)
from ..config import settings


class Md2DocxService:
    def save_markdown(self, id: str, content: str) -> None:
        file = self.get_markdown_file_path(id)

        create_file_directory(file)
        save_file(file, content)

    def save_images(self, id: str, images: list[UploadFile],
                    images_names: Optional[list[Optional[str]]] = None) -> None:
        if images_names is None:
            names = [file.filename for file in images]
        else:
            # TODO: Validate lengths (images and images_names)
            names = [(images_names[i] or images[i].filename) for i in range(len(images))]

        session_dir = self.get_session_dir_by_id(id)

        for image, name in zip(images, names):
            filename = session_dir / name
            save_file_by_chunk(image.file, filename)

    def get_session_dir_by_id(self, id: str) -> Path:
        return settings.SESSION_ROOT / id

    def get_markdown_file_path(self, id: str) -> str:
        return str(self.get_session_dir_by_id(id) / 'md.md')

    def get_docx_file_path(self, id: str) -> str:
        return str(self.get_session_dir_by_id(id) / 'docx.docx')

    def get_pdf_file_path(self, id: str) -> str:
        return str(self.get_session_dir_by_id(id) / 'pdf.pdf')

    def run_processing_tasks(self, id: str) -> None:
        md_file = self.get_markdown_file_path(id)
        docx_file = self.get_docx_file_path(id)

        task = (
            process_md2docx.subtask((md_file, docx_file), task_id=get_task_id(id, TaskType.PROCESSING))
            # | post_process_md2docx.subtask((docx_file,), task_id=get_task_id(id, TaskType.POST_PROCESSING))
        ).apply_async(task_id=id)

    def get_docx_file(self, id: str) -> Optional[tuple[str, str]]:
        path = self.get_docx_file_path(id)

        if not Path(path).is_file():
            return None

        name = uuid.uuid4().hex + '.docx'
        return path, name

    def get_document(self, id: str, doc_format: Literal['docx', 'pdf']):
        file_data = {
            'docx': (self.get_docx_file_path, '.docx'),
            'pdf': (self.get_pdf_file_path, '.pdf'),
        }

        path_getter, ext = file_data[doc_format]
        path = path_getter(id)

        if not Path(path).is_file():
            return None

        name = uuid.UUID(id).hex + ext
        return path, name

    def build_error_message(self, exc: Exception, status: str) -> TaskError:
        result = search_serialized_error(str(exc))

        if result is None:
            return TaskError(error="UnknownError", detail="Unknown error", status=status)

        error, detail = result
        return TaskError(error=error, detail=detail, status=status)


def get_md2docx_service() -> Generator[Md2DocxService, None, None]:
    service = Md2DocxService()
    yield service
