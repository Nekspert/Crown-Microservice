from dataclasses import dataclass

from .dto import TenderReadDTO
from .repository import TenderRepositoryProtocol


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTenderUseCase:
    tenders: TenderRepositoryProtocol

    async def __call__(self, tender_id: int) -> TenderReadDTO:
        tender = await self.tenders.must_get_by_id(tender_id=tender_id)
        return TenderReadDTO.from_entity(tender)
