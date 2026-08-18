from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.adapters.tender_repository import SqlAlchemyTenderRepository

from .db import get_session


def get_tender_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlAlchemyTenderRepository:
    return SqlAlchemyTenderRepository(session=session)
