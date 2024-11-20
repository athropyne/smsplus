from websockets.asyncio.server import ServerConnection

from dto import Event, EventTypes


class Signals:
    @staticmethod
    async def connected(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="connected").model_dump_json())

    @staticmethod
    async def authorized(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="authorized").model_dump_json())

    @staticmethod
    async def disconnected(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="disconnected").model_dump_json())

    @staticmethod
    async def restart(socket: ServerConnection):
        await socket.send(Event(type=EventTypes.SIGNAL, data="connection restarted").model_dump_json())


class Rejects:
    @staticmethod
    async def SecurityServiceConnectionError(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1011, reason="Security service is not available")

    @staticmethod
    async def InvalidToken(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1008, reason="Invalid access token")

    @staticmethod
    async def RedisConnectionError(socket: ServerConnection):
        await Signals.disconnected(socket)
        await socket.close(code=1011, reason="Redis storage is not available")
