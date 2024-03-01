import logging
from enum import Enum

from aiogram.types import Message


class Errors(Enum):
    UNKNOWN = "Неизвестная ошибка"
    SERVER_CONNECTION_ERROR = "Ошибка соединения с сервером"
    SERVER_SIDE_ERROR = "Сервер ответил ошибкой"


class BaseError(BaseException):
    """Базовое исключение для бота"""
    error: str = Errors.UNKNOWN

    async def __new__(cls, message: Message):
        try:
            await message.answer(cls.error)
        except Exception as error:
            logging.error(f"Сообщение об ошибке не отправлено боту: {error}")
        logging.error(cls.error)


class NotConnectedError(BaseError):
    """Исключение при попытке соедениться с сервером"""
    error = Errors.SERVER_CONNECTION_ERROR

class ServerError(BaseError):
    """Исключение при ответе от сервера"""
    error = Errors.SERVER_SIDE_ERROR
