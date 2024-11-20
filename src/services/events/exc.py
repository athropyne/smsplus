from aiohttp import ClientConnectorError


class SecurityServiceConnectionError(Exception):
    def __init__(self, orig: ClientConnectorError):
        self.orig: ClientConnectorError = orig


class InvalidToken(Exception):
    ...
