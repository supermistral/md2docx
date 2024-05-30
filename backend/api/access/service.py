from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from .models import User
from .schemas import User as UserSchema
from .utils import check_password, hash_password
from .exceptions import UserAlreadyExists
from ..db.session import get_session
from ..db.service import BaseDBService
from ..exceptions import NotFoundException


class AccessService(BaseDBService):
    async def get_user_by_email(self, *, email: str) -> User:
        model = await self.db.execute(
            select(User)
            .where(User.email ==  email)
            .where(User.is_active == True)
        )
        return model.scalar_one()

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> User:
        user = await self.get_user_by_email(email=email)

        if not check_password(password, user.password):
            raise NotFoundException(filters=[("email", email)])

        return user

    async def create_user(
        self,
        *,
        schema: UserSchema,
    ) -> User:
        schema.password = hash_password(schema.password)
        model = User(**schema.model_dump())

        self.db.add(model)

        try:
            await self.db.commit()
        except IntegrityError as exc:
            if isinstance(exc.orig.__cause__, UniqueViolationError):
                raise UserAlreadyExists(email=schema.email)
            raise

        return model


async def get_access_service() -> AsyncGenerator[AccessService, None]:
    async with get_session() as session:
        yield AccessService(session)
