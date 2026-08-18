from enum import Enum


class TenderStatus(str, Enum):
    DRAFT = "Черновик"
    ACTIVE = "Активен"
    WON = "Выигран"
    LOST = "Проигран"
