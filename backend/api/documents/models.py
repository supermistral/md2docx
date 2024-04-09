from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from ..db.base import Base
from ..db.mixins import IdMixin


class DocumentTemplate(Base, IdMixin):
    __tablename__ = 'document_templates'

    name: Mapped[str] = mapped_column(sa.String(30))
    content: Mapped[str] = mapped_column(sa.Text, deferred=True)


class DocumentRevision(Base, IdMixin):
    __tablename__ = "document_revisions"

    content: Mapped[str] = mapped_column(sa.Text)
    metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=None)
