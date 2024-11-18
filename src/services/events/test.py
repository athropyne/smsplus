import asyncio

import config
from core.storage import RedisStorage

messages_transfer = RedisStorage(config.MESSAGES_STORAGE_DSN, config.MESSAGES_STORAGE_DB_NAME)


async def main():
    async with messages_transfer as connection:
        while True:
            print("iter")
            await connection.publish("message", "hello")
            await asyncio.sleep(1.5)
            await connection.publish("message", "world")



if __name__ == '__main__':
    asyncio.run(main())
