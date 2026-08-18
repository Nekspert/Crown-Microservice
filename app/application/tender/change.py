from dataclasses import dataclass
from datetime import datetime, timezone

from .dto import ChangeTenderDTO, TenderReadDTO
from .repository import TenderRepositoryProtocol
from ...domain.tender.entities import TenderEntity
from ...domain.tender_history.entities import TenderHistoryEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeTenderStatusUseCase:
    tenders: TenderRepositoryProtocol

    async def __call__(self, dto: ChangeTenderDTO) -> TenderReadDTO:
        tender = await self.tenders.must_get_by_id(tender_id=dto.tender_id)

        now = datetime.now(timezone.utc)
        updated: TenderEntity = tender.with_status(
            new_status=dto.new_status,
            changed_at=now,
        )
        history = TenderHistoryEntity.create(
            tender_id=tender.id,
            changed_by=dto.changed_by,
            old_status=tender.status,
            new_status=updated.status,
            reason=dto.reason,
            changed_at=now,
        )
        await self.tenders.update_status(tender=updated, history=history)
        return TenderReadDTO.from_entity(updated)
