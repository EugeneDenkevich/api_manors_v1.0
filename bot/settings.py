from os import getenv

from dotenv import load_dotenv


load_dotenv()


SERVER_HOST = getenv("SERVER_HOST")
SERVER_PORT = getenv("SERVER_PORT")
BOT_TOKEN = getenv("BOT_TOKEN", "")
WEBHOOK_URL = f"{SERVER_HOST}:{SERVER_PORT}/bot/{BOT_TOKEN}"
SET_WEBHOOK = False
DELETE_WEBHOOK = False
