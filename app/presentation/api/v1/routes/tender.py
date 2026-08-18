from fastapi import APIRouter, Depends
from starlette import status

from app.application.tender.change import ChangeTenderStatusUseCase
from app.application.tender.create import CreateTenderUseCase
from app.application.tender.dto import ChangeTenderDTO, CreateTenderDTO
from app.application.tender.get import GetTenderUseCase
from app.application.tender.history import GetTenderHistoryUseCase
from app.core.config import config
from app.presentation.api.dependencies.use_cases import (
    get_change_tender_status_use_case,
    get_create_tender_use_case,
    get_get_tender_history_use_case,
    get_get_tender_use_case,
)
from app.presentation.api.v1.schemas.tender import (
    TenderCreateSchema,
    TenderHistoryReadSchema,
    TenderReadSchema,
    TenderStatusUpdateSchema,
)

router = APIRouter(
    prefix=config.api.v1.prefix + config.api.v1.tender,
    tags=["Tenders"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TenderReadSchema,
    summary="Создать тендер",
)
async def create_tender(
    body: TenderCreateSchema,
    use_case: CreateTenderUseCase = Depends(get_create_tender_use_case),
):
    dto = await use_case(CreateTenderDTO(**body.model_dump()))
    return TenderReadSchema.model_validate(dto)


@router.patch(
    "/{tender_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=TenderReadSchema,
    summary="Изменить статус тендера",
)
async def change_tender_status(
    tender_id: int,
    body: TenderStatusUpdateSchema,
    use_case: ChangeTenderStatusUseCase = Depends(get_change_tender_status_use_case),
):
    dto = await use_case(ChangeTenderDTO(tender_id=tender_id, **body.model_dump()))
    return TenderReadSchema.model_validate(dto)


@router.get(
    "/{tender_id}",
    status_code=status.HTTP_200_OK,
    response_model=TenderReadSchema,
    summary="Получить тендер",
)
async def get_tender(
    tender_id: int,
    use_case: GetTenderUseCase = Depends(get_get_tender_use_case),
):
    dto = await use_case(tender_id=tender_id)
    return TenderReadSchema.model_validate(dto)


@router.get(
    "/{tender_id}/history",
    status_code=status.HTTP_200_OK,
    response_model=list[TenderHistoryReadSchema],
    summary="История изменений статуса тендера",
)
async def get_tender_history(
    tender_id: int,
    use_case: GetTenderHistoryUseCase = Depends(get_get_tender_history_use_case),
):
    dtos = await use_case(tender_id=tender_id)
    return [TenderHistoryReadSchema.model_validate(dto) for dto in dtos]
