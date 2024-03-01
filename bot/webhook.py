import logging

from bot.settings import SERVER_HOST
from bot.settings import SERVER_PORT
from bot.settings import BOT_TOKEN
from bot.services import bot


async def set_webhook():
    try:
        await bot.set_webhook(
            url=f"{SERVER_HOST}:{SERVER_PORT}/bot/{BOT_TOKEN}",
            drop_pending_updates=True,
        )
    except Exception as e:
        raise Exception(e)
    info = await bot.get_webhook_info()
    logging.info(f"Webhook was successfuly set: {info.url}")
    await bot.session.close()


async def delete_webhook():
    await bot.delete_webhook()
    logging.info(f"Webhook was successfuly deleted")
    