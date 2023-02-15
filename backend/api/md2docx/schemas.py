from enum import Enum
from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class Markdown(BaseModel):
    code: str
    images_names: Optional[list[Optional[str]]] = None


class MarkdownForm:
    def __init__(
        self,
        code: str = Form(...),
        images_names: Optional[list[Optional[str]]] = Form(None)
    ):
        self.code = code
        self.images_names = images_names


class Task(BaseModel):
    status: str


class TaskType(Enum):
    PROCESSING = 1
    WIN_PROCESSING = 2
    POST_PROCESSING = 3
