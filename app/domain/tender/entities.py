from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import ClassVar

from .enums import TenderStatus


@dataclass(frozen=True, slots=True, kw_only=True)
class TenderEntity:
    id: int | None
    title: str
    description: str
    status: TenderStatus
    created_by: int
    created_at: datetime
    updated_at: datetime | None

    allowed_transitions: ClassVar[dict[TenderStatus, set[TenderStatus]]] = {
        TenderStatus.DRAFT: {TenderStatus.ACTIVE},
        TenderStatus.ACTIVE: {TenderStatus.WON, TenderStatus.LOST},
        TenderStatus.WON: set(),
        TenderStatus.LOST: set(),
    }

    @classmethod
    def create(
        cls,
        *,
        title: str,
        description: str,
        created_by: int,
        created_at: datetime,
    ) -> "TenderEntity":
        return cls(
            id=None,
            title=title,
            description=description,
            status=TenderStatus.DRAFT,
            created_by=created_by,
            created_at=created_at,
            updated_at=None,
        )

    def __post_init__(self):
        self._validate_id()
        self._validate_created_by()
        self._validate_title()
        self._validate_created_at()
        self._validate_updated_at()

    def can_change_status(self, new_status: TenderStatus) -> bool:
        return new_status in self.allowed_transitions[self.status]

    def with_status(
        self,
        new_status: TenderStatus,
        changed_at: datetime,
    ) -> "TenderEntity":
        if not self.can_change_status(new_status):
            raise ValueError(
                f"Invalid transition {self.status.value} -> {new_status.value}"
            )
        return replace(self, status=new_status, updated_at=changed_at)

    def _validate_id(self):
        if self.id is not None and self.id <= 0:
            raise ValueError("TenderEntity id must be positive.")

    def _validate_created_by(self):
        if self.created_by <= 0:
            raise ValueError("TenderEntity created by must be positive.")

    def _validate_title(self):
        if not self.title.strip():
            raise ValueError("Tender title cannot be empty.")

    def _validate_created_at(self):
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("TenderEntity created at must be timezone-aware.")
        if self.created_at > datetime.now(timezone.utc):
            raise ValueError("TenderEntity created at cannot be in the future.")

    def _validate_updated_at(self):
        if self.updated_at is None:
            return
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("TenderEntity updated at must be timezone-aware.")
        if self.updated_at > datetime.now(timezone.utc):
            raise ValueError("TenderEntity updated at cannot be in the future.")
