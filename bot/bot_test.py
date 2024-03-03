import telebot
from os import getenv
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = getenv("BOT_TOKEN", "6964981221:AAHgPTqJBl9BSOqe0rYzBD43NHUvkJHF7kI")


bot = telebot.TeleBot(API_TOKEN)


bot.infinity_polling(
    logger_level=logging.DEBUG
)
