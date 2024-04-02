from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
import requests
from requests.exceptions import ConnectionError

from bot.settings import SERVER_HOST
from bot.settings import SERVER_PORT
from bot.settings import TOKEN
from bot.exceptions import NotConnectedError
from bot.exceptions import ServerError


router = Router()


@router.message(CommandStart)
async def start(message: Message) -> None:
    await message.answer("Пошёл запрос на сервер...")
    try:
        url = f"{SERVER_HOST}:{SERVER_PORT}/bot/{TOKEN}"    
        response = requests.post(url, data=dict(message))
        await message.answer(response.text)
    except ConnectionError as error:
        return await NotConnectedError(message)
    except TelegramBadRequest as error:
        return await ServerError(message)
    except Exception as error:
        await message.answer(f"Запрос не прошёл: {error}")
        raise Exception(error)
