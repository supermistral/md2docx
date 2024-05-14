from typing import Optional, Any
from datetime import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..db.base import Base
from ..db.mixins import IdMixin
from ..access.models import User


class MarkdownMetadata(Base):
    __tablename__ = 'users_metadata'

    id = sa.Column(sa.Integer, primary_key=True)
    hash = sa.Column(sa.String(7), nullable=False, unique=True, index=True)
    data = sa.Column(sa.JSON, nullable=False)
    created_date = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated_date = sa.Column(sa.DateTime, nullable=False, default=datetime.now())


class UserDocumentTemplate(Base, IdMixin):
    __tablename__ = "user_document_templates"

    user_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(sa.String(30))
    content: Mapped[str] = mapped_column(sa.Text)

    user: Mapped[User] = relationship()


class UserDocumentHierarchyItem(Base, IdMixin):
    __tablename__ = "user_document_hierarchy_items"

    user_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(sa.String(10))
    content: Mapped[str] = mapped_column(sa.Text)
    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, name="metadata", default=None)
    path: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), default=list)

    user: Mapped[User] = relationship()
