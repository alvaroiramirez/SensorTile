import asyncio
from typing import Any, Awaitable

async def get_result(awaitable: Awaitable) -> str:
    try:
        result = await awaitable
    except Exception as e:
        print("oops!", e)
        return "no result :("
    else:
        return result

f = asyncio.Future()
loop = asyncio.get_event_loop()
loop.call_later(10, f.set_result, "this is my result")
loop.run_until_complete(get_result(f))
