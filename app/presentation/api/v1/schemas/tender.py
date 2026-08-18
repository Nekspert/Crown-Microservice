from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.tender.enums import TenderStatus


class TenderCreateSchema(BaseModel):
    title: str
    description: str
    created_by: int


class TenderReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TenderStatus
    created_by: int
    created_at: datetime
    updated_at: datetime | None


class TenderStatusUpdateSchema(BaseModel):
    new_status: TenderStatus
    reason: str
    changed_by: int


class TenderHistoryReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tender_id: int
    changed_by: int
    old_status: TenderStatus
    new_status: TenderStatus
    reason: str
    changed_at: datetime
