from itertools import chain
from typing import Sequence

from sqlalchemy import RowMapping


class Helper:
    async def convert_users_list_for_redis(self, users: Sequence[RowMapping]):
        return list(chain.from_iterable(r.values() for r in users))

    async def decode_user_list_for_response(self, user_list: dict):
        return [{"id": int(k), "login": v} for k, v in user_list.items()]