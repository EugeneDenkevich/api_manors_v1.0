import asyncio
import redis.asyncio as redis
from bot import bot


async def main():
    connection = redis.Redis()
    topics = ["chat_id",]
    sub = connection.pubsub()
    await sub.subscribe(*topics)
    async for msg in sub.listen():
        if msg["type"] == "message":
            chat_id = int(msg["data"].decode("utf-8").split(":::")[0])
            message = msg["data"].decode("utf-8").split(":::")[1]
            await bot.send_message(
                chat_id=chat_id,
                text=message,
            )


if __name__ == "__main__":
    asyncio.run(main())
