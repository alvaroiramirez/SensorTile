import asyncio
from asyncio.tasks import sleep

async def main():
    print("Alvaro")
    task = asyncio.create_task(foo('text'))
    await task
    print('Finished')

async def foo(text):
    print(text)
    # await asyncio.sleep(1)

if __name__ == "__main__":
    # asyncio.run creates the event-loop that allows the program to run
    asyncio.run(main())