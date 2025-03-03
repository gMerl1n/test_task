from settings.settings import session_local
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_local() as session:
        yield session
