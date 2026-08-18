from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.tender.enums import TenderStatus
from .base import Base
from ..mixins.id_int_pk import IdIntPkMixin


class TenderHistoryModel(Base, IdIntPkMixin):
    __tablename__ = "tender_history"

    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id", onupdate="CASCADE", ondelete="RESTRICT"),
        index=True,
    )
    changed_by: Mapped[int] = mapped_column(index=True)
    old_status: Mapped[str] = mapped_column(Enum(TenderStatus), index=True)
    new_status: Mapped[str] = mapped_column(Enum(TenderStatus), index=True)
    reason: Mapped[str] = mapped_column(TEXT())
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __str__(self):
        return f"<TenderHistory:{self.id}>"
