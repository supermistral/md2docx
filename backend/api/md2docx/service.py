from pathlib import Path
from typing import Generator

from .tasks import process_md2docx, post_process_md2docx
from .schemas import TaskType
from .utils import save_file, get_task_id
from ..config import settings


class Md2DocxService:
    def save_markdown(self, id: str, content: str) -> None:
        session_dir = self.get_session_dir_by_id(id)
        file = session_dir / 'md.md'

        save_file(file, content)

    def get_session_dir_by_id(self, id: str) -> Path:
        return settings.MEDIA_ROOT / 'md2docx' / 'session' / id

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
