import redis
from redis.asyncio import Redis


class RedisStorage:

    def __init__(self,
                 dsn: str,
                 db_name: int):
        self._pool: redis.asyncio.ConnectionPool = redis.asyncio.ConnectionPool.from_url(
            f"{dsn}/{db_name}"
        )
        self.connection: Redis = Redis(connection_pool=self._pool, decode_responses=True)

    async def __aenter__(self):
        self.connection = Redis(connection_pool=self._pool)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    async def __call__(self):
        return self
