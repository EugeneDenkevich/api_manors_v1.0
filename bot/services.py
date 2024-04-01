import redis
from io import BufferedReader

from aiogram import Dispatcher
from aiogram import Bot

from bot.settings import TOKEN
from bot.bot_sync import bot as bot_sync


bot = Bot(token=TOKEN)
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
            bot_sync.send_message(chat_id, message)
        except Exception as e:
            # TODO Обработать ошибку, кода бот посылает сообщение ещё не подключённому юзеру.
            pass
        
    def send_daily_data(self, chat_id: int, daily_data: BufferedReader) -> None:
        """Отправка ботом сообщения"""
        try:
            bot_sync.send_photo(chat_id, daily_data)
        except Exception as e:
            # TODO Обработать ошибку, кода бот посылает сообщение ещё не подключённому юзеру.
            pass


bot_service = BotService()
