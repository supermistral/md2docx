from enum import Enum
from pydantic import BaseModel


class Markdown(BaseModel):
    code: str


class Task(BaseModel):
    status: str


class TaskType(Enum):
    PROCESSING = 1
    WIN_PROCESSING = 2
    POST_PROCESSING = 3
