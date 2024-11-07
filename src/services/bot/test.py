import asyncio


async def task1():
    while True:
        print(1)
        await asyncio.sleep(1)


async def task2():
    while True:
        print(2)
        await asyncio.sleep(2)


async def main():
    asyncio.create_task(task1())
    asyncio.create_task(task2())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.(main())
    loop.run_forever()
