from typing import Generator

from sqlalchemy import select

from .models import DocumentTemplate
from ..db.session import get_session
from ..db.service import BaseDBService


class DocumentsService(BaseDBService):
    async def get_all_document_templates(self) -> list[DocumentTemplate]:
        model = await self.db.execute(
            select(DocumentTemplate)
            .filter(DocumentTemplate.is_active == True)
            .order_by(DocumentTemplate.updated_at.desc())
        )
        return model.scalars().all()


async def get_documents_service() -> Generator[DocumentsService, None, None]:
    async with get_session() as session:
        yield DocumentsService(session)
