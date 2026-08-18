from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.tender.enums import TenderStatus
from .base import Base
from ..mixins.id_int_pk import IdIntPkMixin


class TenderModel(Base, IdIntPkMixin):
    __tablename__ = "tenders"

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(TEXT())
    status: Mapped[str] = mapped_column(Enum(TenderStatus), index=True)
    created_by: Mapped[int] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __str__(self):
        return f"<TenderModel:{self.id}>"
