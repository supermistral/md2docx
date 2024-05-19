from typing import Optional
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..db.base import Base
from ..db.mixins import IdMixin


class User(Base, IdMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(sa.String(50), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(sa.String(50))
    last_name: Mapped[Optional[str]] = mapped_column(sa.String(50))
    password: Mapped[str] = mapped_column(sa.String(255))
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
