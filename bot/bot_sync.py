from telebot import TeleBot
from telebot.types import Message
from os import getenv
from dotenv import load_dotenv
import logging
import httpx

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = getenv("TOKEN")
bot = TeleBot(TOKEN)


@bot.message_handler(commands=["imowner"])
def send_start(message: Message) -> None:
    try:
        wab_app_host = getenv("WEB_APP_HOST", "localhost:8000")
        print()
        print()
        print(wab_app_host)
        print()
        print()
        telegram_id = message.chat.id
        response = httpx.post(
            wab_app_host + "/api/telegram/",
            json={"telegram_id": str(telegram_id)},
        )
        print()
        print()
        print(response.status_code)
        print()
        print()
        print(response.text)
        print()
        print()
        print()
        if response.status_code == 201:
            bot.send_message(
                chat_id=message.chat.id,
                text="✅ Вы добавлены в список владельцев.\n"
                "Теперь вам будут приходить уведомления о заказах.",
            )
        elif response.status_code == 400:
            bot.send_message(
                chat_id=message.chat.id,
                text="⚠️ Вы уже добавлены в базу данных."
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
        allowed_updates=False,
    )
