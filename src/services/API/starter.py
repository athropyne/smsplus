import asyncio
import pathlib
import fastapi_cli.cli

if __name__ == '__main__':

    ### раскомментировать на винде
    import platform
    if platform.system() == "Windows":
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    fastapi_cli.cli.run(pathlib.Path("app.py"))
