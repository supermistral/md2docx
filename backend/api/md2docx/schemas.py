from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Markdown(BaseModel):
    code: str
    images_names: Optional[list[Optional[str]]] = None


class Task(BaseModel):
    status: str


class TaskType(Enum):
    PROCESSING = 1
    WIN_PROCESSING = 2
    POST_PROCESSING = 3
