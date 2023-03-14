from typing import Any

from fastapi import APIRouter, Depends

from .service import UsersService, get_users_service
from .schemas import MarkdownMetadataCreate


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/metadata/{code}')
async def get_config(
    code: str,
    service: UsersService = Depends(get_users_service),
) -> Any:
    metadata = await service.get_metadata(code)
    return metadata


@router.post('/metadata')
async def create_config(
    markdown_metadata_create: MarkdownMetadataCreate,
    service: UsersService = Depends(get_users_service),
) -> Any:
    metadata = await service.create_metadata(markdown_metadata_create)
    return metadata
