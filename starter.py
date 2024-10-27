import asyncio
import pathlib
import threading
from asyncio import WindowsSelectorEventLoopPolicy

import fastapi_cli.cli

from src.bot.main import main

if __name__ == '__main__':

    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    t_api = threading.Thread(target=fastapi_cli.cli.run, args=(pathlib.Path("src/main.py"),))
    t_bot = threading.Thread(target=asyncio.run,args=(main(),))
    t_api.start()
    t_bot.start()
    t_api.join()
    t_bot.join()

    # asyncio.run(main())