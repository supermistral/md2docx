from enum import Enum
from typing import Any, Literal, Union

from pydantic import BaseModel


class MarkdownMetadataErrorType(str, Enum):
    INCORRECT_YAML = 'incorrect_yaml'
    INCORRECT_METADATA = 'incorrect_metadata'
    INCORRECT_METADATA_CODE = 'incorrect_metadata_code'
    NON_EXISTENT_METADATA = 'non_existent_metadata'


class MarkdownMetadataCreate(BaseModel):
    format: Literal['json', 'yaml']
    data: Union[str, dict[str, Any]]


class MarkdownMetadata(BaseModel):
    link: str
    code: str
    full_code: str
