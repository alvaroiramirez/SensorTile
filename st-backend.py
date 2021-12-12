## IMPORTS
from io import TextIOWrapper

# Bluetooth connectivity
import asyncio
from bleak import BleakClient

# Unpack sensor data
import struct

# keyboard management
from aiokeyboard import async_input_without_enter_needed  # Also available: async_input_requiring_enter

# import time
from datetime import datetime

# GUI
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu

# App configuration
from stconfig import DEVICE_MAC, HANDLE_READ_DATA, SHOW_VALUES_ON_SCREEN, FILE_TYPE


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
        # raw data format: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
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

        print('About to stop notification...')

        try:
            await self.client.stop_notify(char)
        except Exception as e:
            print(f"Error: {e}")

        print('Notification stopped')


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
        if print_status == "recording":
            if SHOW_VALUES_ON_SCREEN:
                print("")
                print(f"cnt: {cnt}   Time Stamp: {datetime_stamp}")
                print(f"ACC X: {self.acc[0]}   ACC Y: {self.acc[1]}   ACC Z: {self.acc[2]}")
                print(f"GYR X: {self.gyr[0]}   GYR Y: {self.gyr[1]}   GYR Z: {self.gyr[2]}")
                print(f"MAG X: {self.mag[0]}   MAG Y: {self.mag[1]}   MAG Z: {self.mag[2]}")
                print(f"Raw data: {self.rawdata}")

            if FILE_TYPE == 'EDGE':
                # Record for Edge Impulse - Timestamp and sensor data only
                self.data_file.write(f"{self.timeStamp},{self.acc[0]},{self.acc[1]},{self.acc[2]},{self.gyr[0]},{self.gyr[1]},{self.gyr[2]},{self.mag[0]},{self.mag[1]},{self.mag[2]}\n")
            else:
                # Full data file version
                self.data_file.write(f"{cnt},{self.timeStamp},{exercise},{sample},{self.acc[0]},{self.acc[1]},{self.acc[2]},{self.gyr[0]},{self.gyr[1]},{self.gyr[2]},{self.mag[0]},{self.mag[1]},{self.mag[2]},{self.rawdata}\n")



# Store datetime stamp for filename
def setInitialDateTimeStamp():

    global datetime_stamp

    # datetime_stamp = time.localtime()
    datetime_stamp = datetime.now()


# Generate the name of the file using the system's current time
def openFile():

    global exercise

    filename = ".\\data\\" + \
        datetime_stamp.strftime('%y%m%d') + "_" + \
        datetime_stamp.strftime('%H%M%S') + "_" + \
        '{:0>2}'.format(exercise) + "_" + \
        '{:0>2}'.format(sample) + ".csv"

    file = open(filename, "w")

    # Full data file version
    if FILE_TYPE == 'EDGE':
        # Titles for Edge Impulse file version
        title = "timestamp,"
        title += "ACC X,ACC Y,ACC Z,"
        title += "GYR X,GYR Y,GYR Z,"
        title += "MAG X,MAG Y,MAG Z\n"
    else:    
        # All titles
        title = "cnt, timestamp, exercise, sample, "
        title += "ACC X, ACC Y, ACC Z, "
        title += "GYR X, GYR Y, GYR Z, "
        title += "MAG X, MAG Y, MAG Z, "
        title += "raw\n"

    file.write(f"{title}")

    return file


# Obtain the number of the exercise to record
async def menu():

    global exercise

    # Display options
    print("Menu")
    print("====")
    print("")
    print("1 - Leg up and down")
    print("2 - Knee facing up")
    print("3 - Knee facing down")
    print("x - Exit")
    print("")

    while True:
        key = await async_input_without_enter_needed()

        if key in (b'x', 'x'):      # Exit
            exercise = -1
            break
        elif key in (b'123'):  # Exercise selected
            exercise = int(key)
            break

    return key


# Generate data to train the model
async def mainControl(client):
    
    global print_status, exercise, sample

    if client is None:
        raise Exception(f"Could not find device with BLE address {client}")
    
    try:
        # Initialize process
        setInitialDateTimeStamp()
        key = await menu()
        if key in (b'x', 'x'):   # User selected the exit option
            return

        print_status = "ready"
        print(f"   Ready to start exercise {exercise}!")

        # Start notifications
        await client.start_notification(HANDLE_READ_DATA)
        
        while True:
            # Keyboard management
            key = await async_input_without_enter_needed()

            if key in (b'x', 'x'):          # Exit
                if print_status == "recording":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                    client.data_file.close()
                    print('File closed')

                print("Data collection terminated")
                break

            elif key in (b's', 's'):          # Start collecting data
                if print_status != "recording":
                    sample += 1
                    print(f"      Start data collection exercise {exercise} / sample {sample}...")
                    print_status = "recording"
            
                    client.data_file = openFile()

            elif key in (b'e', 'e'):          # Stop data collection
                if print_status == "recording":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                    print_status = "stopped"
                    client.data_file.close()
                    print('File closed')
            
            elif key in (b'm', 'm'):          # Prepare system for new exercise
                if print_status != "ready":
                    if print_status == "recording":
                        print(f"      ...End data collection exercise {exercise} / sample {sample}")
                        client.data_file.close()
                        print('File closed')

                    key = await menu()
                    if key in (b'x', 'x'):      # User selected the exit option
                        break
                    else:
                        print(f"   Ready to start exercise {exercise}")
                    
                    print_status = "ready"
                    sample = 0

        # Stop notifications
        await client.stop_notification(HANDLE_READ_DATA)

    except Exception as e:
        print(f"AIR Error: {e}")

    finally:
        try:
            client.data_file.close()
            print('File closed')
        except:
            pass

    print('Data capture complete')


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
    await mainControl(st2)

    # GUI
    # app.exec()

    # Closes the process
    print("Process complete.")
    

if __name__ == "__main__":

    asyncio.run(main())
