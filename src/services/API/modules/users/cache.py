from typing import List

from fastapi import Depends
from redis import StrictRedis

from core.storages import users_cache, RedisStorage


class Cache:
    def __init__(self,
                 storage: RedisStorage = Depends(users_cache)):
        self.storage = storage

    async def list(self) -> dict:
        """Возвращает `список` пользователей из кэша в виде словаря словарей"""
        async with self.storage as c:
            return await c.hgetall("users")

    async def add(self, user: List[int | str]):
        """Добавляет пользователя в кэш"""
        async with self.storage as c:
            await c.hset("users", items=user)

    async def fill(self, users_data: List[int | str]):
        """Заполняет кэш всеми пользователями из базы"""
        async with self.storage as c:
            await c.hset("users", items=users_data)
