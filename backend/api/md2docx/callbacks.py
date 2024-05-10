import asyncio
from typing import Any

from .service import get_md2docx_service


def done_failed_processing(
    self: Any,
    exc: Exception,
    task_id: str,
    args: tuple[Any],
    kwargs: dict[str, Any],
    einfo: Any,
):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _done_failed_processing(
            exc=exc,
            operation_id=kwargs["operation_id"],
        )
    )


async def _done_failed_processing(
    *,
    exc: Exception,
    operation_id: str,
):
    async for service in get_md2docx_service():
        await service.done_failed_processing(
            exc=exc,
            operation_id=operation_id,
        )
