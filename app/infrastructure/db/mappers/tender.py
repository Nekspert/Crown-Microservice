from app.domain.tender.entities import TenderEntity
from app.infrastructure.db.models.tender import TenderModel


def model_to_entity(model: TenderModel) -> TenderEntity:
    return TenderEntity(
        id=model.id,
        title=model.title,
        description=model.description,
        status=model.status,
        created_by=model.created_by,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def entity_to_model(entity: TenderEntity) -> TenderModel:
    return TenderModel(
        id=entity.id,
        title=entity.title,
        description=entity.description,
        status=entity.status,
        created_by=entity.created_by,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
