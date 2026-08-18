from dataclasses import dataclass
from datetime import datetime

from app.domain.tender.entities import TenderEntity
from app.domain.tender.enums import TenderStatus
from app.domain.tender_history.entities import TenderHistoryEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class TenderReadDTO:
    id: int
    title: str
    description: str
    status: TenderStatus
    created_by: int
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, entity: TenderEntity) -> "TenderReadDTO":
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class TenderHistoryReadDTO:
    id: int
    tender_id: int
    changed_by: int
    old_status: TenderStatus
    new_status: TenderStatus
    reason: str
    changed_at: datetime

    @classmethod
    def from_entity(cls, entity: TenderHistoryEntity) -> "TenderHistoryReadDTO":
        return cls(
            id=entity.id,
            tender_id=entity.tender_id,
            changed_by=entity.changed_by,
            old_status=entity.old_status,
            new_status=entity.new_status,
            reason=entity.reason,
            changed_at=entity.changed_at,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTenderDTO:
    title: str
    description: str
    created_by: int


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeTenderDTO:
    tender_id: int
    new_status: TenderStatus
    reason: str
    changed_by: int
