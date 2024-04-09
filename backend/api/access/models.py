from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base
from ..db.mixins import IdMixin


class User(Base, IdMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(sa.String(50), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(sa.String(30))
    last_name: Mapped[Optional[str]] = mapped_column(sa.String(30))
    password: Mapped[Optional[str]] = mapped_column(sa.String(30), deferred=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
