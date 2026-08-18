from dataclasses import dataclass
from datetime import datetime, timezone

from .dto import CreateTenderDTO, TenderReadDTO
from .repository import TenderRepositoryProtocol
from ...domain.tender.entities import TenderEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTenderUseCase:
    tenders: TenderRepositoryProtocol

    async def __call__(self, dto: CreateTenderDTO) -> TenderReadDTO:
        tender = await self.tenders.save(
            tender=TenderEntity.create(
                title=dto.title,
                description=dto.description,
                created_by=dto.created_by,
                created_at=datetime.now(timezone.utc),
            ),
        )
        return TenderReadDTO.from_entity(tender)
