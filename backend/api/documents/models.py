import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func

from ..db.base import Base
from ..db.mixins import IdMixin


class DocumentTemplate(Base, IdMixin):
    __tablename__ = 'document_templates'

    name: Mapped[str] = mapped_column(sa.String(30))
    content: Mapped[str] = mapped_column(sa.Text, deferred=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)


class DocumentRevision(Base, IdMixin):
    __tablename__ = "document_revisions"

    content: Mapped[str] = mapped_column(sa.Text)
    storage_images_paths: Mapped[Optional[str]] = mapped_column(sa.Text, default=None)
    operation_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("operations.id"))
