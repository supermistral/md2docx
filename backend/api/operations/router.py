from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException

from .service import OperationService, get_operation_service
from .dependencies import verify_session
from .utils import generate_created_by
from . import schemas


router = APIRouter(
    prefix='/operations',
    tags=['operations'],
    dependencies=[Depends(verify_session)],
)


@router.get('/{operation_id}', response_model=schemas.OperationResponse)
async def get_operation(
    operation_id: str,
    request: Request,
    service: OperationService = Depends(get_operation_service),
):
    operation = await service.get_by_id(operation_id)

    # TODO: add completed auth permission check (from JWT/etc)
    created_by = generate_created_by(request=request)

    if created_by != operation.created_by:
        raise HTTPException(401, detail="Unauthorized")

    return operation
