## IMPORTS
from io import TextIOWrapper
from stconfig import DEVICE_MAC, HANDLE_READ_DATA, SHOW_VALUES_ON_SCREEN

import asyncio
import struct
import time
import logging
from bleak import BleakClient, BleakError, BleakScanner

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu

# from pynput.keyboard import Key, Listener

import keyboard


# GLOBAL VARIABLES
print_status = ""
cnt = 0
exercise = 0
sample = 0
datetime_stamp = 0


## CLASSES
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()


    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


class Device():
    __name: str
    __mac: str
    __rawdata: str   # This is not a string. Update.
    
    #Sensors data
    timeStamp = ""
    acc = [0, 0, 0]
    gyr = [0, 0, 0]
    mag = [0, 0, 0]
    # data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    data_file: TextIOWrapper

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
        self.data = asyncio.LifoQueue(maxsize=1)


    async def connect(self):
        # Connect to SensorTile
        await self.client.connect()

        # Ensure connection was established
        assert self.client.is_connected, "Device is not connected"


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

        # *** I want to confirm that this coroutine stops notifications ***

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


    def read_data(self, param, data):

        # *** Note: I need to check what is param ***

        global print_status, cnt, exercise

        # Line counter
        cnt += 1

        """Simple notification handler which prints the data received."""
        result = struct.unpack_from("<hhhhhhhhhh", data)

        self.rawdata = data

        # Time stamp
        self.timeStamp = result[0]

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
        if print_status == "s":
            if SHOW_VALUES_ON_SCREEN:
                print("")
                print(f"cnt: {cnt}   Time Stamp: {self.timeStamp}   Raw data: {self.rawdata}")
                print(f"ACC X: {self.acc[0]}   ACC Y: {self.acc[1]}   ACC Z: {self.acc[2]}")
                print(f"GYR X: {self.gyr[0]}   GYR Y: {self.gyr[1]}   GYR Z: {self.gyr[2]}")
                print(f"MAG X: {self.mag[0]}   MAG Y: {self.mag[1]}   MAG Z: {self.mag[2]}")

            self.data_file.write(f"{cnt}, {self.timeStamp}, {exercise}, {sample}, \
                {self.acc[0]}, {self.acc[1]}, {self.acc[2]},\
                {self.gyr[0]}, {self.gyr[1]}, {self.gyr[2]},\
                {self.mag[0]}, {self.mag[1]}, {self.mag[2]},\
                {self.rawdata}\n")
        

# Store datetime stamp for filename
def setInitialDateTimeStamp():

    global datetime_stamp

    datetime_stamp = time.localtime()


# Generate the name of the file using the system's current time
def openFile():

    global exercise

    updateExerciseNumber()

    filename = ".\\data\\" + \
        time.strftime('%y%m%d', datetime_stamp) + "_" + \
        time.strftime('%H%M%S', datetime_stamp) + "_" + \
        '{:0>2}'.format(exercise) + ".csv"

    file = open(filename, "w")

    title = "cnt, time stamp, exercise, sample, "
    title += "ACC X, ACC Y, ACC Z, "
    title += "GYR X, GYR Y, GYR Z, "
    title += "MAG X, MAG Y, MAG Z, "
    title += "raw\n"

    file.write(f"{title}")

    return file


# Obtain the number of the exercise to record
def updateExerciseNumber():

    global exercise

    # Display options
    print("Menu")
    print("====")
    print("")
    print("1 - Leg up and down")
    print("2 - Knee facing up")
    print("3 - Knee facing down")
    print("")

    exercise = int(input())
    

# Generate data to train the model
async def generateData(client):
    
    global print_status, exercise, sample

    try:
        setInitialDateTimeStamp()

        # Initialize keyboard status
        if print_status == "":
            client.data_file = openFile()

            print_status = "r"
            print(f"   Ready to start exercise {exercise}!")

        await client.start_notification(HANDLE_READ_DATA)
        
        while True:
            await asyncio.sleep(0)

            # Keyboard management
            if keyboard.is_pressed("x"):    # Exit
                if print_status == "s":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                print("Data collection terminated")
                break

            elif keyboard.is_pressed("s"):  # Start collecting data
                if print_status != "s":
                    sample += 1
                    print(f"      Start data collection exercise {exercise} / sample {sample}...")
                    print_status = "s"
            
            elif keyboard.is_pressed("e"):  # Stop data collection
                if print_status == "s":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                    print_status = "e"
            
            elif keyboard.is_pressed("n"):  # Prepare system for new exercise
                if print_status != "r":
                    if print_status == "s":
                        print(f"      ...End data collection exercise {exercise} / sample {sample}")

                    client.data_file.close()
                    print('File closed')

                    client.data_file = openFile()

                    sample = 0
                    print(f"   Ready to start exercise {exercise}")
                    print_status = "r"
                
        print('About to stop notification...')
        await client.stop_notification(HANDLE_READ_DATA)
        print('Notification stopped')

    except Exception as e:
        print(f"AIR Error: {e}")

    else:
        client.data_file.close()
        print('File closed')

    print('Data capture complete')
    return


async def main():

    # GUI
    # app = QApplication([])
    # window = MainWindow()
    # window.show()

    # Register device
    print("Registering device...")
    st2 = Device(DEVICE_MAC)

    # Connect device
    print("Connecting device...")
    await st2.connect()

    # Read and process data
    print("Starting testing...")
    await generateData(st2)

    # GUI
    # app.exec()

    # Closes the process
    print("Process complete.")
    
    return


if __name__ == "__main__":

    asyncio.run(main())