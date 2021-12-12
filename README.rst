=====
SensorTile - Bleak
=====

.. figure:: https://raw.githubusercontent.com/hbldh/bleak/master/Bleak_logo.png
    :target: https://github.com/hbldh/bleak
    :alt: Bleak Logo
    :scale: 50%


.. image:: https://github.com/hbldh/bleak/workflows/Build%20and%20Test/badge.svg
    :target: https://github.com/hbldh/bleak/actions?query=workflow%3A%22Build+and+Test%22
    :alt: Build and Test

.. image:: https://img.shields.io/pypi/v/bleak.svg
    :target: https://pypi.python.org/pypi/bleak

.. image:: https://readthedocs.org/projects/bleak/badge/?version=latest
    :target: https://bleak.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

This software uses Bleak (by Henrik Blidth) to connect a SensorTile with a Windoows computer via bluetooth. The system obtains the following data:

- Record count
- datetime stamp
- Exercise number
- Sample number
- Accelerometer data (X, Y, Z)
- Gyroscope data (X, Y, Z)
- Magnetometer data (X, Y, Z)
- Raw data


----

Bleak is an acronym for Bluetooth Low Energy platform Agnostic Klient.

* Free software: MIT license
* Documentation: https://bleak.readthedocs.io.

Bleak is a GATT client software, capable of connecting to BLE devices
acting as GATT servers. It is designed to provide a asynchronous,
cross-platform Python API to connect and communicate with e.g. sensors.
