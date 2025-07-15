import enum


class ClientErrorMessage(enum.StrEnum):
    EXTERNAL_API_ERROR = "Ошибка внешнего API"
    HERO_NOT_FOUND_ERROR = "Герой не найден"
    HERO_ALREADY_EXISTS_ERROR = "Все найденые герои уже существуют в БД"
