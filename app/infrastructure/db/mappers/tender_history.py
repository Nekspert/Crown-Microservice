from app.domain.tender_history.entities import TenderHistoryEntity
from app.infrastructure.db.models.tender_history import TenderHistoryModel


def model_to_history(model: TenderHistoryModel) -> TenderHistoryEntity:
    return TenderHistoryEntity(
        id=model.id,
        tender_id=model.tender_id,
        changed_by=model.changed_by,
        old_status=model.old_status,
        new_status=model.new_status,
        reason=model.reason,
        changed_at=model.changed_at,
    )


def history_to_model(history: TenderHistoryEntity) -> TenderHistoryModel:
    return TenderHistoryModel(
        id=history.id,
        tender_id=history.tender_id,
        changed_by=history.changed_by,
        old_status=history.old_status,
        new_status=history.new_status,
        reason=history.reason,
        changed_at=history.changed_at,
    )
