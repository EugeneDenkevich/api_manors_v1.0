from telebot import TeleBot
import redis

from bot.settings import BOT_TOKEN


bot = TeleBot(token=BOT_TOKEN)


class BotService:
    """Сервис бота"""
    
    def send_message_redis(self, chat_id, message) -> None:
        """Отправка ботом сообщения используя Redis"""
        connection = redis.Redis()     
        connection.publish("chat_id", f"{str(chat_id)}:::{str(message)}")
        # TODO Сделать создание connection в другом месте.

    def send_message(self, chat_id, message) -> None:
        """Отправка ботом сообщения"""
        bot.send_message(chat_id=chat_id, text=message)


bot_service = BotService()
