import uuid
from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..db.base import Base
from ..db.mixins import IdMixin
from ..operations.models import Operation


class DocumentTemplate(Base, IdMixin):
    __tablename__ = 'document_templates'

    name: Mapped[str] = mapped_column(sa.String(30))
    content: Mapped[str] = mapped_column(sa.Text, deferred=True)


class DocumentRevision(Base, IdMixin):
    __tablename__ = "document_revisions"

    content: Mapped[str] = mapped_column(sa.Text)
    metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=None)
    operation_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("operations.id"))

    operation: Mapped[Operation] = relationship(
        back_populates="document_revision",
        single_parent=True,
    )
