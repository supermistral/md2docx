from datetime import datetime
import sqlalchemy as sa

from ..db.base import Base


class MarkdownMetadata(Base):
    __tablename__ = 'users_metadata'

    id = sa.Column(sa.Integer, primary_key=True)
    hash = sa.Column(sa.String(7), nullable=False, unique=True, index=True)
    data = sa.Column(sa.JSON, nullable=False)
    created_date = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    updated_date = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
