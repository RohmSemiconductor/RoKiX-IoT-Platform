## Copyright ® 2017-2022 ROHM Semiconductor
## ROHM EVK version 3.0.1 release
## 11.02.2022
## https://www.rohm.com/support/accelerometer-evk-support


## Folder structure
ROHM-EVK-Docs
* user guides and other documents
ROHM-EVK-Firmware
* latest firmware binary for CY8CKIT059, Arduino and nRF52840-DK
ROHM-EVK-GUI
* ROHM EVK GUI application and default configurations

## System Requirements
* Windows 10 (Windows 8.1 and Windows 7 also supported)
* Preferred minimum display resolution (1920 x 1080)


## Change log
Release version 3.0.1
# New functionality:
* new connection states in top right corner: EVK Disconnected, EVK Connected, EVK Ready, EVK Mismatch

# Fixes and updates:
* renewed user guides
* configuration download logic improved
* GUI layout updates
* about host adapter window shows all possible firmware infomation

# Known issues:
* COM port scanning takes sometimes long time which slows down the auto connect functionality
* GPIO toggling may have some perfomance problems during data streaming

Release version 2.6
* logarithmic x & y on FFT plot
* support for BU79100G-LA-EVK-001 ADC converter

Release version 2.3
* support for Kionix accelerometers
