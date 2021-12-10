"""
Lesson 9

Write name of device

"""

import asyncio
from bleak import BleakScanner, BleakClient

async def main(address):
     """Write to characteristics"""
     device = await BleakScanner.find_device_by_address(address)

     if device is None:
         raise Exception(f"Could not find device with BLE address {address}")
     async with BleakClient(device) as client:
         print(f"Connected: {client.is_connected}")

         # MTU (Maximum Transfer Unit) Size limits how many bytes you can send
         # in one write (and get in one read).
         print(f"MTU Size: {client.mtu_size}")

         data_pre_write = await client.read_gatt_char(6)
         print(f"Data value pre-write: {data_pre_write}")
        #  await client.write_gatt_char(8, b'\x00\x01', response=False)
         await client.write_gatt_char(6, b'Device1', response=True)
         data_post_write = await client.read_gatt_char(6)
         print(f"Data value post-write: {data_post_write}")

         config_pre_write = await client.read_gatt_char(6)
         print(f"Config value pre-write: {config_pre_write}")
         await client.write_gatt_char(6, b'Device 1+', response=False)
         config_post_write = await client.read_gatt_char(6)
         print(f"Config value post-write: {config_post_write}")

         await asyncio.sleep(10.0)

     print(f"Connected: {client.is_connected}")

asyncio.run(main(address="C0:83:48:32:4A:36"))
