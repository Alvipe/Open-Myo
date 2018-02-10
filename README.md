# Open-Myo
Python module to get data from a Myo armband using a generic Bluetooth LE interface.

## Installation and usage

This module works with generic Bluetooth LE antennas (e.g. CSR V4.0, Cambridge Silicon Radio or the Bluetooth interface integrated in the Raspberry Pi 3/Raspberry Pi Zero W). This module does not work with the Bluetooth antenna included with the Myo armband because it uses a propietary protocol from Bluegiga. 

This module requires the [bluepy](https://github.com/IanHarvey/bluepy) Python module to work. To install it, run:

``$ sudo pip install bluepy``

All code using the bluepy module must run with root permissions. To run the example code, execute:

``$ sudo python main.py``

The Open Myo module **only works on Linux**, as the bluepy module is only available for Linux.

## Acknowledgements

Thanks to [mamo91](https://github.com/mamo91) and [MyrikLD](https://github.com/MyrikLD), since your Dongleless-myo code ([here](https://github.com/mamo91/Dongleless-myo) and [here](https://github.com/MyrikLD/Dongleless-myo)) has served as a starting point for this project. Thank you both for sharing your work! :D

Also thanks to [IanHarvey](https://github.com/IanHarvey) for developing the fantastic bluepy module.

