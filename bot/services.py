import redis

from aiogram import Dispatcher
from aiogram import Bot
import redis
from telebot import TeleBot

from bot.settings import BOT_TOKEN
from bot.bot_sync import bot as bot_sync


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class BotService:
    """Сервис бота"""
    
    def send_message_redis(self, chat_id, message) -> None:
        """Отправка ботом сообщения используя Redis"""
        connection = redis.Redis()     
        connection.publish("chat_id", f"{str(chat_id)}:::{str(message)}")
        # TODO Сделать создание connection в другом месте.

    def send_message(self, chat_id, message) -> None:
        """Отправка ботом сообщения"""
        try:
            bot_sync.send_message(chat_id=chat_id, text=message)
        except:
            # TODO Обработать ошибку, кода бот посылает сообщение ещё не подключённому юзеру.
            pass


bot_service = BotService()
