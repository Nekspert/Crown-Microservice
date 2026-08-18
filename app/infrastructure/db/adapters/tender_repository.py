from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.tender.repository import TenderRepositoryProtocol
from app.domain.tender.entities import TenderEntity
from app.domain.tender_history.entities import TenderHistoryEntity
from app.infrastructure.db.mappers.tender import entity_to_model, model_to_entity
from app.infrastructure.db.mappers.tender_history import (
    history_to_model,
    model_to_history,
)
from app.infrastructure.db.models.tender import TenderModel
from app.infrastructure.db.models.tender_history import TenderHistoryModel


@dataclass(frozen=True, slots=True, kw_only=True)
class SqlAlchemyTenderRepository(TenderRepositoryProtocol):
    session: AsyncSession

    async def must_get_by_id(self, tender_id: int) -> TenderEntity:
        model = await self.session.get(TenderModel, tender_id)
        if model is None:
            raise KeyError(f"Tender {tender_id} not found.")
        return model_to_entity(model)

    async def save(self, tender: TenderEntity) -> TenderEntity:
        model = entity_to_model(tender)
        self.session.add(model)
        await self.session.commit()
        return model_to_entity(model)

    async def update_status(self, tender: TenderEntity, history: TenderHistoryEntity):
        model = await self.session.get(TenderModel, tender.id)
        model.status = tender.status.name
        model.updated_at = tender.updated_at
        self.session.add(history_to_model(history))
        await self.session.commit()

    async def get_history(self, tender_id: int) -> list[TenderHistoryEntity]:
        stmt = (
            select(TenderHistoryModel)
            .where(TenderHistoryModel.tender_id == tender_id)
            .order_by(TenderHistoryModel.changed_at.desc())
        )
        rows = (await self.session.scalars(stmt)).all()
        return [model_to_history(model) for model in rows]
