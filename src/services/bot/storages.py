from redis.asyncio import Redis

import config


class RedisStorage:

    def __init__(self,
                 host: str,
                 port: int,
                 db):
        self.connection: Redis = Redis(host=host,
                                       port=port,
                                       db=db,
                                       decode_responses=True)


message_transfer = RedisStorage(config.MESSAGE_TRANSFER_REDIS_HOST(),
                                config.MESSAGE_TRANSFER_REDIS_PORT(),
                                config.MESSAGE_TRANSFER_REDIS_DBNAME())
