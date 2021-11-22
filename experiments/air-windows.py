import asyncio
import numpy as np

from pyqtgraph.Qt import QtCore, QtGui
# import PyQt6
from asyncqt import QEventLoop, asyncSlot
import pyqtgraph as pg

from bleak import BleakClient

from stconfig import DEVICE_MAC

# BLE peripheral ID
UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class Window(pg.GraphicsLayoutWidget):
    def __init__(self, loop=None, parent=None):
        super().__init__(parent)
        self._loop = loop

        self.setWindowTitle("pyqtgraph example: Scrolling Plots")
        plot = self.addPlot()
        self._data = np.zeros(5)
        self._curve = plot.plot(self.data)
        self._client = BleakClient(DEVICE_MAC, loop=self._loop)

    @property
    def client(self):
        return self._client

    async def start(self):
        await self.client.connect()
        self.start_read()

    async def stop(self):
        await self.client.disconnect()

    @property
    def data(self):
        return self._data

    @property
    def curve(self):
        return self._curve

    async def read(self):
        data = await self.client.read_gatt_char(UUID)
        sensor_data = data.split(",")
        if len(sensor_data) >= 5:
            temperature_str = sensor_data[4]
            try:
                temperature = float(temperature_str)
            except ValueError as e:
                print(f"{temperature_str} not is float")
            else:
                self.update_plot(temperature)
        QtCore.QTimer.singleShot(5000, self.start_read)

    def start_read(self):
        asyncio.ensure_future(self.read(), loop=self._loop)

    def update_plot(self, temperature):
        self.data[:-1] = self.data[1:]
        self.data[-1] = temperature
        self.curve.setData(self.data)

    def closeEvent(self, event):
        super().closeEvent(event)
        asyncio.ensure_future(self.client.stop(), loop=self._loop)


def main(args):
    app = QtGui.QApplication(args)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = Window()
    window.show()

    with loop:
        asyncio.ensure_future(window.start(), loop=loop)
        loop.run_forever()


if __name__ == "__main__":
    import sys

    main(sys.argv)