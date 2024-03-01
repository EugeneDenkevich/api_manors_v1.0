from pathlib import Path
import sys

BOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BOT_DIR))

import logging
import asyncio

from bot.settings import SET_WEBHOOK
from bot.settings import DELETE_WEBHOOK
from bot.routers import router
from bot.webhook import set_webhook
from bot.webhook import delete_webhook
from bot.services import bot, dp


logging.basicConfig(level=logging.INFO)

async def main():
    dp.include_router(router)
    if DELETE_WEBHOOK:
        await delete_webhook()
        exit()
    if SET_WEBHOOK:
        await set_webhook()
    else:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
