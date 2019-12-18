# Temperature-Monitor

![Temperature-Monitor screenshot](https://raw.githubusercontent.com/Caff1982/Temperature-Monitor/images/screenshot.jpg)

Temperature-Monitor is designed to monitor the temperature of devices in Linux computers. The GUI allows you to monitor the temperatures live and it can also log the results to a CSV file. The refresh rate can be set by the user and the devices can be enabled/disabled using the 'Devices' menu.

This program is designed to spot any heating issues over extended periods of time. Most similar application I found seemed to be focused more on real-time data and did not allow for logging of temperatures. 

# Installation + Usage

This program requires Python 3 to run. 

* Install the Python requirements with pip install -r requirements.txt
* Run the program with python main.py

The program displays all the devices found in the /sys/class/hwmon/ folder on Linux computers. Devices can be enabled/disabled using the 'Device' menu. The devices may be in different directories depending on the kernel and hardware being used.

The refresh rate can be set using the GUI. I would not recommend setting this below 1 second as it may cause some lagging. 

The temperature is plotted for the first device by default, this can be changed in the 'Tools' menu. The temperature is taken every second and plotted every five seconds.

The CSV file will create a log for all the active devices. To create separate CSV files for each device you can use 'Open New Window' from the file menu for each required device. 

# Contributing

Any issues and Pull Requests are welcome. 




