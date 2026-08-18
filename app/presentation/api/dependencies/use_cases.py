from fastapi import Depends

from app.application.tender.change import ChangeTenderStatusUseCase
from app.application.tender.create import CreateTenderUseCase
from app.application.tender.get import GetTenderUseCase
from app.application.tender.history import GetTenderHistoryUseCase
from app.infrastructure.db.adapters.tender_repository import SqlAlchemyTenderRepository

from .repositories import get_tender_repository


def get_create_tender_use_case(
    repository: SqlAlchemyTenderRepository = Depends(get_tender_repository),
) -> CreateTenderUseCase:
    return CreateTenderUseCase(tenders=repository)


def get_change_tender_status_use_case(
    repository: SqlAlchemyTenderRepository = Depends(get_tender_repository),
) -> ChangeTenderStatusUseCase:
    return ChangeTenderStatusUseCase(tenders=repository)


def get_get_tender_use_case(
    repository: SqlAlchemyTenderRepository = Depends(get_tender_repository),
) -> GetTenderUseCase:
    return GetTenderUseCase(tenders=repository)


def get_get_tender_history_use_case(
    repository: SqlAlchemyTenderRepository = Depends(get_tender_repository),
) -> GetTenderHistoryUseCase:
    return GetTenderHistoryUseCase(tenders=repository)
