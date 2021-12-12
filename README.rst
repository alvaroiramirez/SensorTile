=====
SensorTile - Bleak
=====

This software uses Bleak (by Henrik Blidth) to connect a SensorTile with a Windows computer via bluetooth. The system obtains the following data:

- Record count
- datetime stamp
- Exercise number
- Sample number
- Accelerometer data (X, Y, Z)
- Gyroscope data (X, Y, Z)
- Magnetometer data (X, Y, Z)
- Raw data

Version 1.5.1 allows to record n samples of up to three exercises:

1 - Leg up and down
2 - Knee facing up
3 - Knee facing down

The data is stored in .csv format.

------

Bleak is an acronym for Bluetooth Low Energy platform Agnostic Klient.

* Free software: MIT license
* Documentation: https://bleak.readthedocs.io.

Bleak is a GATT client software, capable of connecting to BLE devices
acting as GATT servers. It is designed to provide a asynchronous,
cross-platform Python API to connect and communicate with e.g. sensors.
