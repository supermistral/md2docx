from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Operation
from .schemas import OperationCreate
from ..db.session import get_session


class OperationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, operation_id: str) -> Operation:
        result = await self.db.execute(
            select(Operation).filter(Operation.id == operation_id)
        )
        return result.scalar_one()

    async def create(self, schema: OperationCreate) -> Operation:
        model = Operation(
            created_by=schema.created_by,
        )

        self.db.add(model)
        await self.db.commit()

        return model


async def get_operation_service() -> AsyncGenerator[OperationService, None]:
    async with get_session() as session:
        yield OperationService(session)
