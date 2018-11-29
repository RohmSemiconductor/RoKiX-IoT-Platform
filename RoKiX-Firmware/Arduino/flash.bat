@echo Arduino Firmware update tool
@set /p comport="Enter Arduino COM port number: "
@set /p avrdude_dir="Enter avrdude directory: "
@%avrdude_dir%\avrdude.exe -patmega328p -carduino -PCOM%comport% -b115200 -D  -Uflash:w:"kionix-arduino-firmware-latest-release.hex":i -C%avrdude_dir%\avrdude.conf
pause
