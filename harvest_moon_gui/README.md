# Harvest Moon PyQT5 GUI
## Warning
This is a work in progress GUI.

## Overview

![Alt text](documentation/screenshot.png?raw=true "Screenshot")

A quick and simple pyqt5 gui for displaying sensor data from the sensor suite.

## Dependencies
Before running the script, you should install PyQT5's binaries by:

```
sudo apt install pyqt5-dev-tools
```

## Running the script

The script searches for the `custom_reader.py` script via relative path. So, please do run the script in the directory structure as you `git pull`-ed.

Currently, one UI instance only supports one sensor suite (The arduino nano or arduino uno)

Remember to specify the `port_num` and `baud_rate` as `sys.argv[1]` amd `sys.argv[2]` arguments. Normally, `/dev/ttyUSB0` is arduino nano and `/dev/ttyACM0` is arduino uno.Baud rate currently tied down to 9600.

```
python3 harvest_moon_py_qt_gui.py /dev/ttyUSB0 9600
```
or
```
python3 harvest_moon_py_qt_gui.py /dev/ttyACM0 9600
```
