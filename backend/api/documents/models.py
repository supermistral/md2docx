import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped

from ..db.base import Base
from ..db.mixins import IdMixin


class DocumentTemplate(Base, IdMixin):
    __tablename__ = 'document_templates'

    name: Mapped[str] = mapped_column(sa.String(30))
    content: Mapped[str] = mapped_column(sa.Text, deferred=True)


class DocumentRevision(Base, IdMixin):
    __tablename__ = "document_revisions"

    content: Mapped[str] = mapped_column(sa.Text)
    storage_images_paths: Mapped[Optional[str]] = mapped_column(sa.Text, default=None)
    operation_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("operations.id"))
