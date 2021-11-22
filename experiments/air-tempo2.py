import asyncio
from stconfig import DEVICE_MAC
from bleak import discover

async def run():
    devices = await discover()
    for d in devices:
        if d.address == DEVICE_MAC:
            print(f"Address : {d.address}")
            print(f"Name    : {d.name}")            
            print(f"Metadata: {d.metadata}")            
            print(f"RSSI    : {d.rssi}")            


loop = asyncio.get_event_loop()
loop.run_until_complete(run())