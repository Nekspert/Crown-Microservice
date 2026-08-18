from dataclasses import dataclass

from .dto import TenderHistoryReadDTO
from .repository import TenderRepositoryProtocol


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTenderHistoryUseCase:
    tenders: TenderRepositoryProtocol

    async def __call__(self, tender_id: int) -> list[TenderHistoryReadDTO]:
        await self.tenders.must_get_by_id(tender_id=tender_id)
        entities = await self.tenders.get_history(tender_id=tender_id)
        return [TenderHistoryReadDTO.from_entity(entity) for entity in entities]
