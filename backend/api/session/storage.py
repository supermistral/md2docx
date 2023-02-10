import uuid
from typing import Optional

import aioredis

from ..config import settings


class SessionStorage:
    def __init__(self):
        self.client = aioredis.from_url(settings.SESSION_BACKEND_URL, decode_responses=True)

    async def session_exists(self, session_id: str) -> bool:
        return await self.client.get(session_id) is not None

    async def add_session(self, session_id: str, session_key: str) -> None:
        return await self.client.set(session_id, session_key)

    async def get_session(self, session_id: str) -> str:
        return await self.client.get(session_id)

    async def del_session(self, session_id: str) -> None:
        return await self.client.delete(session_id)

    def get_session_from_cookies(self, cookies: dict[str, str]) -> Optional[str]:
        return cookies.get(settings.SESSION_COOKIE)

    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    async def generate_session_id(self) -> str:
        id = self._generate_id()

        while await self.session_exists(id):
            id = self._generate_id()

        return id


def get_session_storage() -> SessionStorage:
    return SessionStorage()


session_storage = get_session_storage()
