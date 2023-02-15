from pathlib import Path
from typing import Generator, Optional

from fastapi import UploadFile

from .tasks import process_md2docx, post_process_md2docx
from .schemas import TaskType
from .utils import save_file, get_task_id, save_file_by_chunk, create_file_directory
from ..config import settings


class Md2DocxService:
    def save_markdown(self, id: str, content: str) -> None:
        session_dir = self.get_session_dir_by_id(id)
        file = session_dir / 'md.md'

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

    def run_processing_tasks(self, id: str) -> None:
        md_file = self.get_markdown_file_path(id)
        docx_file = self.get_docx_file_path(id)

        task = (
            process_md2docx.subtask((md_file, docx_file), task_id=get_task_id(id, TaskType.PROCESSING))
            # | post_process_md2docx.subtask((docx_file,), task_id=get_task_id(id, TaskType.POST_PROCESSING))
        ).apply_async(task_id=id)


def get_md2docx_service() -> Generator[Md2DocxService, None, None]:
    service = Md2DocxService()
    yield service
