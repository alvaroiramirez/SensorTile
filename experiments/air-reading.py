"""
ST Reader - Draft 1
-------------------

Example under construction to read data from one device

Created on 2021-11-10 by Alvaro Ramirez

"""

import sys
import platform
import asyncio
import logging
import binascii
import struct

# from bleak_winrt.windows.foundation import AsyncActionCompletedHandler

from bleak import BleakClient
from bleak import BleakScanner
from stconfig import DEVICE_MAC, CHAR_RW

ACTION     = "R"                                    # R: Read   W: Write   RW: Read & Write

async def air_list_services(client):
    for service in client.services:
        print(f"[Service] {service}")
        for char in service.characteristics:
            if "read" in char.properties:
                try:
                    print()
                    value = bytes(await client.read_gatt_char(char.uuid))
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")
                except Exception as e:
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")

            else:
                value = None
                print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

            for descriptor in char.descriptors:
                try:
                    value = bytes(
                        await client.read_gatt_descriptor(descriptor.handle)
                    )
                    print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                except Exception as e:
                    print(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


async def process_all():
    stiles = []

    print("Discovering devices...")
    devices = await BleakScanner.discover()
    print(f"{devices.count} device(s) found")
    for d in devices:
        # print("Device " + d.name)

        # Read characteristics using air_list_services
        # if d.name[0:5] == 'STILE':
        # if d.name[0:5] == 'AM1V3':
            stiles.append(d)
            print("Device " + d.address + ' ' + d.name + " found!")

            try:
                async with BleakClient(d.address) as client:
                    print(f"Connected: {client.is_connected}")

                    # Read services list for this client
                    await air_list_services(client)

                    # Read GATT char: char-read-hnd 000e
                    print("GATT Char")
                    # await air_char_management_test(client)        # **** I'm here ****

            except Exception as e:
                print(f"Error: {e}")

            else:
                print("Connection succesful")

            finally:
                print("Connection process complete")


async def process_one(device_mac):
    print(f"Searching for {device_mac}...")

    try:
        async with BleakClient(device_mac) as client:
            print(f"Connected: {client.is_connected}")

            # Read services list for this client
            await air_list_services(client)

            # Read/write GATT char: char-read-hnd 000e
            print("Writing characteristic...")
            
            # Test values
            exit_loop = False
            value = ''

            while not exit_loop:
                try:
                    # Read current value
                    current_value = bytes(await client.read_gatt_char(CHAR_RW))
                    print(f"Original value: {current_value}")

                    if ACTION == "W" or ACTION == "RW":
                        value = read_user_value()

                        if value == "X":
                            exit_loop = True

                        else:
                            print(f"Value to write: {value}")
                            await client.write_gatt_char(CHAR_RW, value, True)

                    if value != "X":
                        # Read new value
                        current_value = bytes(await client.read_gatt_char(CHAR_RW))
                        print(f"New value: {current_value}")

                        if ACTION == "R":
                            value = read_user_value()
                            if value == "X":
                                exit_loop = True

                except Exception as e:
                    print(f"Error: {e}")
                    value = read_user_value()
                    if value == "X":
                        exit_loop = True

                else:
                    print("Connection succesful")

                finally:
                    print("Connection process complete")

    except Exception as e:
        print(f"Error: {e}")

    else:
        print("Connection succesful")

    finally:
        print("Connection process complete")


def read_user_value():
    data = int(input("Enter new characteristic to be tested: "))
    return data


async def read_char_ST(char):
    async with BleakClient(DEVICE_MAC) as client:
            try:
                value = bytes(await client.read_gatt_char(char))
                print(value)
            except Exception as e:
                print(f"Error: {e}")


async def write_char_ST(value):
    async with BleakClient(DEVICE_MAC) as client:
            try:
                # await client.connect()
                await client.write_gatt_char(6, value)
                # await client.write_gatt_char('00002a00-0000-1000-8000-00805f9b34fb', value)
                # bytes(await client.write_gatt_char('00000012-0000-1000-8000-00805f9b34fb', value))
            except Exception as e:
                print(f"Error: {e}")


async def test():
    try:
        async with BleakClient(DEVICE_MAC) as client:
                handle = int(input("Notification handle: "))
                await start_notification(client, handle)
                # asyncio.sleep(0.1)
                input("Continue? ")

                await stop_notification(client, handle)

    except Exception as e:
        print(f"Error: {e}")


async def start_notification(client, char):
        try:
            await client.start_notify(char, notification_handler)
        except Exception as e:
            print(f"Error: {e}")


async def stop_notification(client, char):
        try:
            await client.stop_notify(char)
        except Exception as e:
            print(f"Error: {e}")


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    result = struct.unpack_from("<hhhhhhhhhh", data)
    print("")
    print(data)
    print(result)

    # Acceleration
    acc_x = struct.unpack_from("<h", data[2:4])
    acc_y = struct.unpack_from("<h", data[4:6])
    acc_z = struct.unpack_from("<h", data[6:8])    
    print(f"ACC X: {acc_x}   ACC Y: {acc_y}   ACC Z: {acc_z}")

    # Gyroscope
    gyr_x = struct.unpack_from("<h", data[8:10])
    gyr_y = struct.unpack_from("<h", data[10:12])
    gyr_z = struct.unpack_from("<h", data[12:14])
    print(f"GYR X: {gyr_x}   GYR Y: {gyr_y}   GYR Z: {gyr_z}")

    # Magnetometer
    mag_x = struct.unpack_from("<h", data[14:16])
    mag_y = struct.unpack_from("<h", data[16:18])
    mag_z = struct.unpack_from("<h", data[18:20])
    print(f"MAG X: {mag_x}   MAG Y: {mag_y}   MAG Z: {mag_z}")


async def main():
    # await test()

    # await process_one(DEVICE_MAC)
    await process_all()
    # device_name = 'ABC'
    # char1 = '00002a00-0000-1000-8000-00805f9b34fb'
    # char2 = '00002a01-0000-1000-8000-00805f9b34fb'
    # char3 = '00002a04-0000-1000-8000-00805f9b34fb'
    # char4 = '00140000-0001-11e1-ac36-0002a5d5c51b'
    # char5 = int(6)

    # await read_char_ST(16)
    # await read_char_ST(char1)
    # await read_char_ST(char2)
    # await read_char_ST(char3)
    # await read_char_ST(char4)
    # await read_char_ST(char5)

    # await write_char_ST(bytearray(map(ord, 'ABC')))
    # await write_char_ST(bytearray(map(ord, bytearray(b'\x01\x00'))))

    # await write_char_ST(bytearray(b'01234567'))
    # await write_char_ST(bytearray(b'ABC', 'UTF-8'))


    # await write_char_ST(bytearray('ABC', 'UTF-8'))
    # await write_char_ST('ST1')
    # await write_char_ST(bytes(b'ABC'))
    # await write_char_ST(bytes('ABC', 'UTF-8'))
    # await write_char_ST('ST1')

    # await read_char_ST()

asyncio.run(main())