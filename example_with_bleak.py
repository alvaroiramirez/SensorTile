"""

Simple keyboard reading example with Bleak

"""


import asyncio
from aiokeyboard import async_input_requiring_enter, async_input_without_enter_needed

from bleak import BleakScanner, BleakClient


KEY_PRESS_HANDLE = 75
LIGHT_SENSOR_DATA = 67
LIGHT_SENSOR_CONFIG = 70


def callback(sender: int, data: bytearray):
    """Simplest callback possible. Print data received."""
    print(f"{sender}: {data}")


async def main(address):
    device = await BleakScanner.find_device_by_address(address)
    
    if device is None:
        raise Exception(f"Could not find device with BLE address {address}")
    
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")

        # "Waking" the sensor and starting notifications from it.
        # await client.write_gatt_char(LIGHT_SENSOR_CONFIG, bytearray([1,]))
        await client.start_notify(LIGHT_SENSOR_DATA, callback)
        print("Sleeping...")

    while True:
        # Use the one that you feel most comfortable with.
        key = await async_input_without_enter_needed()
        # key = await async_input_requiring_enter()

        if key in (b'q', 'q'):
            break

        print("Done sleeping.")

        # Stopping notifications and "turning off" the sensor again.
        await client.stop_notify(LIGHT_SENSOR_DATA)
        await client.write_gatt_char(LIGHT_SENSOR_CONFIG, bytearray([0,]))

    print(f"Connected: {client.is_connected}")

asyncio.run(main(address="C0:83:48:32:4A:36"))
