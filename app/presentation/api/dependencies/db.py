from typing import Any, AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.database import AsyncDatabaseManager


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, Any]:
    manager: AsyncDatabaseManager = request.app.state.manager
    async with manager.async_sessionmaker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
