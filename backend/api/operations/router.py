import logging

from fastapi import APIRouter, Depends, HTTPException

from .service import OperationService, get_operation_service
from .dependencies import verify_session
from . import schemas
from ..users.utils import generate_created_by

LOG = logging.getLogger(__name__)


router = APIRouter(
    prefix="/operations",
    tags=["operations"],
    dependencies=[Depends(verify_session)],
)


@router.get("/{operation_id}", response_model=schemas.OperationResponse)
async def get_operation(
    operation_id: str,
    service: OperationService = Depends(get_operation_service),
    created_by: str = Depends(generate_created_by),
):
    operation = await service.get_by_id(operation_id)

    # TODO: add completed auth permission check (from JWT/etc)

    if created_by != operation.created_by:
        LOG.warning("User %s is not author of the operation %s", created_by, operation.id)
        raise HTTPException(401, detail="Unauthorized")

    return operation


@router.get("/", response_model=schemas.ListOperationsResponse)
async def get_all_operations(
    service: OperationService = Depends(get_operation_service),
    created_by: str = Depends(generate_created_by),
):
    operations = await service.get_all_by_created_by(created_by)

    return schemas.ListOperationsResponse(
        operations=operations,
    )
