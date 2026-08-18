from typing import Protocol

from ...domain.tender.entities import TenderEntity
from ...domain.tender_history.entities import TenderHistoryEntity


class TenderRepositoryProtocol(Protocol):
    async def must_get_by_id(self, tender_id: int) -> TenderEntity:
        pass

    async def save(self, tender: TenderEntity) -> TenderEntity:
        pass

    async def update_status(self, tender: TenderEntity, history: TenderHistoryEntity):
        pass

    async def get_history(self, tender_id: int) -> list[TenderHistoryEntity]:
        pass
