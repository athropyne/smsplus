import asyncio
import pathlib
from asyncio import WindowsSelectorEventLoopPolicy

import fastapi_cli.cli

if __name__ == '__main__':
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    fastapi_cli.cli.run(
        pathlib.Path("src/main.py")
    )