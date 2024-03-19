from telebot import TeleBot
from telebot.types import Message
from os import getenv
from dotenv import load_dotenv
import logging
import requests
import sqlite3


load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = getenv("BOT_TOKEN", "6731870799:AAEmVFfFWWiJrdJzLJB76QZtDFCE6NVwK2w")

bot = TeleBot(API_TOKEN)

conn = sqlite3.connect('Owners.db')
cur = conn.cursor()

@bot.message_handler(commands=["imowner"])
def send_start(message: Message) -> None:
    try:
        telegram_id = message.chat.id
        cur.execute("INSERT INTO Owners (telegram_id) VALUES (?) ON CONFLICT DO NOTHING", (telegram_id,))
        conn.commit()
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ Вы добавлены в список владельцев.\n"
                 "Теперь вам будут приходить уведомления о заказах."
        )
    except sqlite3.IntegrityError:
        bot.send_message(
            chat_id=message.chat.id,
            text="❌ Вы уже добавлены в список владельцев\n."
        )
    except Exception as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ Извините, произошла ошибка: {e}\n"
                    "Мы не смогли добавить вас в список владельцев."
        )

if __name__ == "__main__":
    logging.info("SYNC BOT STARTED")
    bot.infinity_polling(
        logger_level=logging.INFO,
    )
