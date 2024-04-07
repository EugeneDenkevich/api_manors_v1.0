from io import BufferedReader

from bot.bot_sync import bot


class SyncBotService:
    """Сервис бота"""

    def send_message(self, chat_id, message) -> None:
        """Отправка ботом сообщения"""
        try:
            bot.send_message(chat_id, message)
        except Exception as e:
            raise Exception()
        
    def send_daily_data(self, chat_id: int, daily_data: BufferedReader) -> None:
        """Отправка ботом ежедневной таблицы"""
        try:
            bot.send_photo(chat_id, daily_data)
        except Exception as e:
            raise Exception()


bot_service = SyncBotService()
