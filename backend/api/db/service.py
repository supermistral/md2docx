from sqlalchemy.ext.asyncio import AsyncSession


class BaseDBService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
