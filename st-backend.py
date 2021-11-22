## imports
from stconfig import DEVICE_MAC, HANDLE_READ_DATA
import asyncio
import struct
import logging
from bleak import BleakClient, BleakError, BleakScanner

## CLASSES
class Device():
    __name: str
    __mac: str
    __rawdata: str   # This is not a string. Update.
    acc = [0, 0, 0]
    gyr = [0, 0, 0]
    mag = [0, 0, 0]
    # data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


    # Properties
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def mac(self):
       return self.__mac

    @mac.setter
    def mac(self, value):
        self.__mac = value

    @property
    def rawdata(self): 
        return self.__rawdata

    @rawdata.setter
    def rawdata(self, value):
        self.__rawdata = value


    # Methods
    def __init__(self, mac):
        self.__mac = mac
        self.client = BleakClient(self.__mac)

        # This line generates RuntimeError: asyncio.run() cannot be called from a running event loop. 
        # asyncio.run(self.connect())
        # print(f"Connected in __init__()?: {self.client.is_connected}")

        # A LiFo Queue will ensure that the most recent registered
        # ST data is retrieved
        # self.data = asyncio.LifoQueue(maxsize=1)        


    async def connect(self):
        # Connect to SensorTile
        await self.client.connect()

        # Ensure connection was established
        assert self.client.is_connected, "Device is not connected"


    # no_async_connect generates RuntimeWarning: coroutine 'BleakClientWinRT.connect' was never awaited
    # I leave this function here just to remember why async def connect() is needed
    # def no_async_connect(self):
    #     # Connect to SensorTile
    #     self.client.connect()

    #     # Ensure connection was established
    #     assert self.client.is_connected, "Device is not connected"


    async def list_services(self):

        # Verify that device is connected
        if not self.client.is_connected:
            print(f"{self.mac} is not connected in list_services().")
            return

        for service in self.client.services:
            print(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        print()
                        value = bytes(await self.client.read_gatt_char(char.uuid))
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")
                    except Exception as e:
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")

                else:
                    value = None
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await self.client.read_gatt_descriptor(descriptor.handle)
                        )
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


    async def stop_notification(self, char):
        try:
            await self.client.stop_notify(char)
        except Exception as e:
            print(f"Error: {e}")


    async def start_notification(self, char):
        try:
            task = asyncio.create_task(self.client.start_notify(char, self.read_data))
            await task

        except Exception as e:
            print(f"AIR Error: {e}")


    def test_read_data():
        # Newest version
        print("I'm reading...")


    def read_data(self, param, data):
        """Simple notification handler which prints the data received."""
        result = struct.unpack_from("<hhhhhhhhhh", data)

        self.rawdata = data

        # Acceleration
        self.acc[0] = result[1]
        self.acc[1] = result[2]
        self.acc[2] = result[3]

        # Gyroscope
        self.gyr[0] = result[4]
        self.gyr[1] = result[5]
        self.gyr[2] = result[6]

        # Magnetometer
        self.mag[0] = result[7]
        self.mag[1] = result[8]
        self.mag[2] = result[9]

        # Display results
        print("")
        print(f"Raw data: {self.rawdata}")
        print(f"ACC X: {self.acc[0]}   ACC Y: {self.acc[1]}   ACC Z: {self.acc[2]}")
        print(f"GYR X: {self.gyr[0]}   GYR Y: {self.gyr[1]}   GYR Z: {self.gyr[2]}")
        print(f"MAG X: {self.mag[0]}   MAG Y: {self.mag[1]}   MAG Z: {self.mag[2]}")


async def test(client):
    try:
        await client.start_notification(HANDLE_READ_DATA)
        await asyncio.sleep(1)
        print('Process complete')

        await client.stop_notification(HANDLE_READ_DATA)

    except Exception as e:
        print(f"AIR Error: {e}")


async def main():

    # Register device
    print("Registering device...")
    st2 = Device(DEVICE_MAC)

    # Connect device
    print("Connecting device...")
    await st2.connect()

    # Read and process data
    print("Starting testing...")
    await test(st2)

    # Closes the process
    print("Process complete.")
    

if __name__ == "__main__":
    # main()
    asyncio.run(main())