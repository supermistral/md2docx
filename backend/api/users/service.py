import random
import string
import yaml
from datetime import datetime
from typing import Any, AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from md2docx.pandoc.helpers import validate_metadata_from_dict

from .utils import to_base64, from_base64
from .models import MarkdownMetadata as MarkdownMetadataModel
from .schemas import (
    MarkdownMetadata, MarkdownMetadataCreate,
    MarkdownMetadataErrorType
)
from ..config import settings
from ..exceptions import BaseException
from ..db.session import get_session


class UsersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.markdown_metadata_hash_length = MarkdownMetadataModel.hash.type.length

    def _generate_metadata_hash(self) -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(self.markdown_metadata_hash_length))

    async def _generate_free_metadata_hash(self) -> str:
        hash = self._generate_metadata_hash()

        while (
            (await self.db.execute(
                select(MarkdownMetadataModel).filter(MarkdownMetadataModel.hash == hash)
            )).scalar() is not None
        ):
            hash = self._generate_metadata_hash()

        return hash

    def _build_yaml_error_message(self, exc: yaml.YAMLError) -> str:
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            return f"Error at the position: line {mark.line + 1}, column {mark.column + 1}"
        return "Unknown error while parsing yaml"

    def _raise_error(self, error_type: MarkdownMetadataErrorType, **kwargs) -> None:
        status = 400

        if error_type == MarkdownMetadataErrorType.INCORRECT_YAML:
            detail=self._build_yaml_error_message(kwargs.get('exception', None))
        elif error_type == MarkdownMetadataErrorType.INCORRECT_METADATA:
            exception = kwargs.get('exception', None)
            if exception is not None:
                # TODO: probably add __call__() to the error interface
                # instead of 'str(exception)' do 'exception()'
                detail = str(exception)
            else:
                detail = "An unknown error has occured"
        elif error_type == MarkdownMetadataErrorType.INCORRECT_METADATA_CODE:
            detail = ("Incorrect metadata code. Make sure you entered "
                      "the correct code or base64 encoded string")
        else:
            status = 404
            detail = "Metadata for this code was not found"

        raise BaseException(
            status_code=status,
            error_type=error_type.value,
            detail=detail
        )

    async def create_metadata(self, metadata: MarkdownMetadataCreate) -> MarkdownMetadata:
        if metadata.format == 'yaml':
            try:
                data = yaml.load(metadata.data)
            except yaml.YAMLError as exc:
                return self._raise_error(MarkdownMetadataErrorType.INCORRECT_YAML, exception=exc)
        else:
            data = metadata.data

        try:
            validate_metadata_from_dict(data)
        except Exception as exc:
            return self._raise_error(MarkdownMetadataErrorType.INCORRECT_METADATA, exception=exc)

        hash = await self._generate_free_metadata_hash()
        model = MarkdownMetadataModel(hash=hash, data=data)

        self.db.add(model)
        await self.db.commit()

        return MarkdownMetadata(
            link=f'{settings.FRONTEND_BASE_URL}/?metadata={hash}',
            code=hash,
            full_code=to_base64(data)
        )

    async def _find_and_update_metadata_entry(self, hash: str) -> MarkdownMetadataModel:
        result = await self.db.execute(
            select(MarkdownMetadataModel).filter(MarkdownMetadataModel.hash == hash)
        )
        model = result.scalar()

        if model is None:
            return self._raise_error(MarkdownMetadataErrorType.NON_EXISTENT_METADATA)

        model.updated_date = datetime.now()
        await self.db.commit()

        return model

    async def get_metadata(self, code: str) -> dict[str, Any]:
        # Check if hash exists in db
        if len(code) == self.markdown_metadata_hash_length:
            model = await self._find_and_update_metadata_entry(code)
            return model.data

        # It's base64 encoded metadata string
        try:
            metadata = from_base64(code)
        except Exception as exc:
            return self._raise_error(MarkdownMetadataErrorType.INCORRECT_METADATA_CODE)

        try:
            validate_metadata_from_dict(metadata)
        except Exception as exc:
            return self._raise_error(MarkdownMetadataErrorType.INCORRECT_METADATA, exception=exc)

        return metadata


async def get_users_service() -> AsyncGenerator[UsersService, None]:
    async with get_session() as session:
        yield UsersService(session)
