import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from ...core.config import PostgresqlConfig
from ...infrastructure.db.models.base import Base

logger = logging.getLogger(__name__)


class AsyncDatabaseManager:
    def __init__(self, async_url: str):
        logger.debug("Initialize PostgreSQL manager")

        self.async_url = async_url
        self.async_engine: AsyncEngine | None = None
        self.async_sessionmaker: async_sessionmaker[AsyncSession] | None = None

    async def connect(self):
        if not self.async_engine:
            self.async_engine = create_async_engine(
                self.async_url,
                pool_pre_ping=True,
            )
        if not self.async_sessionmaker:
            self.async_sessionmaker = async_sessionmaker(
                bind=self.async_engine,
                autoflush=False,
                expire_on_commit=False,
            )
        await self.log_db_version()

    async def log_db_version(self):
        try:
            async with self.async_engine.connect() as conn:
                result = await conn.execute(text("SELECT version();"))
                logger.info(f"Connected to Async PostgreSQL version: {result.scalar()}")
        except Exception as e:
            logger.exception(f"Failed to connect Async PostgreSQL: {e}")
            raise

    async def async_create_all(self, base: Base):
        async with self.async_engine.begin() as conn:
            conn.run_sync(base.metadata.create_all)

    async def close(self):
        if self.async_engine is not None:
            await self.async_engine.dispose()
            logger.info("Async PostgreSQL connection pool closed")


def build_async_db_manager(config: PostgresqlConfig) -> AsyncDatabaseManager:
    return AsyncDatabaseManager(async_url=config.database_url_asyncpg)
