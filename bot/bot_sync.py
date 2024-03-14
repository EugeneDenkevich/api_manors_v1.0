from telebot import TeleBot
from telebot.types import Message
from os import getenv
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = getenv("BOT_TOKEN", "6964981221:AAHgPTqJBl9BSOqe0rYzBD43NHUvkJHF7kI")


bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=["imowner"])
def send_start(message: Message) -> None:
    try:
        # TODO Реализовать добавление id владельца в БД.
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ Вы добавлены в список владельцев.\n"
                 "Теперь вам будут приходить уведомления о заказах."
        )
    except:
        # TODO Реализовать исключение, когда пользователь уже в БД
        bot.send_message(
            chat_id=message.chat.id,
            text="❌ Извините, произошла ошибка\n."
                 "Мы не смогли добавить вас в базу данных."
        )

if __name__ == "__main__":
    logging.info("SYNC BOT STARTED")    
    bot.infinity_polling(
        logger_level=logging.INFO,
    )
