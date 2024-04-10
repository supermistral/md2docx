from typing import Any, Optional
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from ..db.base import Base
from ..db.mixins import IdMixin
from .schemas import OperationStatus


class Operation(Base, IdMixin):
    __tablename__ = "operations"

    status: Mapped[str] = mapped_column(default=OperationStatus.PENDING)
    response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=None)
    error: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=None)
    metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=None)
    created_by: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
    )
    updated_at = Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
    )
