from telebot import TeleBot
from telebot.types import Message
from os import getenv
from dotenv import load_dotenv
import logging
import requests

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = getenv("BOT_TOKEN", "6731870799:AAEmVFfFWWiJrdJzLJB76QZtDFCE6NVwK2w")

bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=["imowner"])
def send_start(message: Message) -> None:
    try:
        telegram_id = message.chat.id
        response = requests.post(
            "http://127.0.0.1:8000/authentication",
            json={"user_id": telegram_id, "username": message.from_user.username},
        )

        if response.status_code == 200:
            bot.send_message(
                chat_id=message.chat.id,
                text="✅ Вы добавлены в список владельцев.\n"
                "Теперь вам будут приходить уведомления о заказах.",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="❌ Произошла ошибка при добавлении в базу данных.",
            )
    except Exception as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ Извините, произошла ошибка: {e}\n"
            "Мы не смогли добавить вас в список владельцев.",
        )


if __name__ == "__main__":
    logging.info("SYNC BOT STARTED")
    bot.infinity_polling(
        logger_level=logging.INFO,
    )
