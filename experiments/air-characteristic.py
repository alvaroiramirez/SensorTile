import asyncio
from bleak import BleakClient

address = "C0:83:48:32:4A:36"
MODEL_NBR_UUID = "00140000-0001-11e1-ac36-0002a5d5c51b"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))