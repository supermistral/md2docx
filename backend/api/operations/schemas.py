import uuid
from enum import Enum
from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from ..modeling import BaseResponse


class OperationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCECSS = "success"
    FAILED = "failed"


class Operation(BaseModel):
    id: uuid.UUID
    status: OperationStatus = OperationStatus.PENDING
    response: Optional[dict[str, Any]] = None
    error: Optional[dict[str, Any]] = None
    metadata_: Optional[dict[str, Any]] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OperationCreate(Operation):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class OperationResponse(BaseResponse):
    id: uuid.UUID
    status: OperationStatus
    response: Optional[dict[str, Any]]
    error: Optional[dict[str, Any]]
    metadata_: Optional[dict[str, Any]] = Field(..., serialization_alias="metadata")
    created_at: datetime
    updated_at: datetime


class ListOperationsResponse(BaseResponse):
    operations: list[OperationResponse]
