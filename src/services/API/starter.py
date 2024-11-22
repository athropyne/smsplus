import asyncio
import pathlib
import sys

import fastapi_cli.cli

from core import config

if __name__ == '__main__':
    config.is_dev(True if "dev" in sys.argv else False)
    import platform
    if platform.system() == "Windows":
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    fastapi_cli.cli.run(pathlib.Path("app.py"))
