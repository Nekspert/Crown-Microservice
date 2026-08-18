from dataclasses import dataclass
from datetime import datetime, timezone

from ...domain.tender.enums import TenderStatus


@dataclass(frozen=True, slots=True, kw_only=True)
class TenderHistoryEntity:
    id: int | None
    tender_id: int
    changed_by: int
    old_status: TenderStatus
    new_status: TenderStatus
    reason: str
    changed_at: datetime

    @classmethod
    def create(
        cls,
        *,
        tender_id: int,
        changed_by: int,
        old_status: TenderStatus,
        new_status: TenderStatus,
        reason: str,
        changed_at: datetime,
    ) -> "TenderHistoryEntity":
        return cls(
            id=None,
            tender_id=tender_id,
            changed_by=changed_by,
            old_status=old_status,
            new_status=new_status,
            reason=reason,
            changed_at=changed_at,
        )

    def __post_init__(self):
        self._validate_id()
        self._validate_tender_id()
        self._validate_changed_by()
        self._validate_changed_at()

    def _validate_id(self):
        if self.id is not None and self.id <= 0:
            raise ValueError("TenderHistoryEntity id must be positive.")

    def _validate_tender_id(self):
        if self.tender_id <= 0:
            raise ValueError("TenderHistoryEntity tender id must be positive.")

    def _validate_changed_by(self):
        if self.changed_by <= 0:
            raise ValueError("TenderHistoryEntity changed by must be positive.")

    def _validate_changed_at(self):
        if self.changed_at.tzinfo is None or self.changed_at.utcoffset() is None:
            raise ValueError("TenderHistoryEntity changed at must be timezone-aware.")
        if self.changed_at > datetime.now(timezone.utc):
            raise ValueError("TenderHistoryEntity changed at cannot be in the future.")
