from enum import Enum
from typing import Any, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OperationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCECSS = "success"
    FAILED = "failed"


class OperationCreate(BaseModel):
    created_by: str


class Operation(BaseModel):
    id: UUID
    status: OperationStatus = OperationStatus.PENDING
    response: Optional[dict[str, Any]] = None
    error: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class OperationResponse(BaseModel):
    id: UUID
    status: OperationStatus
    response: Optional[dict[str, Any]]
    error: Optional[dict[str, Any]]
    metadata: Optional[dict[str, Any]]
    created_at: datetime
    updated_at: datetime
