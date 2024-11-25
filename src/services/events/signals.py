from websockets.asyncio.server import ServerConnection

from core.config import logger
from dto import Event, EventTypes


class Signals:
    @staticmethod
    async def connected(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="connected").model_dump_json())
        logger.info(f"клиент {socket.id} подключен")

    @staticmethod
    async def authenticated(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="authorized").model_dump_json())
        logger.info(f"клиент {socket.id} аутентифицирован")

    @staticmethod
    async def disconnected(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="disconnected").model_dump_json())
        logger.info(f"клиент {socket.id} отключен")

    @staticmethod
    async def restart(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="connection restarted").model_dump_json())
        logger.info(f"клиент {socket.id} подключен заново")


class Rejects:
    @staticmethod
    async def SecurityServiceConnectionError(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1011, reason="Security service is not available")
        logger.debug(f"клиент {socket.id} отключен из за неверного недоступного сервиса аутентификации")

    @staticmethod
    async def InvalidToken(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1008, reason="Invalid access token")
        logger.debug(f"клиент {socket.id} отключен из за неверного токена доступа")

    @staticmethod
    async def RedisConnectionError(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1011, reason="Redis storage is not available")
