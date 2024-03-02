from asgiref.sync import async_to_sync
from aiogram import Dispatcher
from aiogram import Bot
import redis

from bot.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class BotService:
    """Сервис бота"""
    
    def send_message(self, chat_id, message) -> None:
        """Отправка ботом сообщения"""
        connection = redis.Redis()
        connection.publish("chat_id", f"{str(chat_id)}:::{str(message)}")
        # TODO Сделать создание connection в другом месте.

bot_service = BotService()
