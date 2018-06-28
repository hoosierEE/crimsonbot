#!/usr/bin/env bash
# reset a NodeMCU to "standard micropython"

PORT=$(ls /dev/tty.* | grep -i usb)  # should work on linux and macos (sorry Windows users)
BIN=$(ls *.bin)                      # don't put more than one .bin file in here or this will break

esptool.py --port $PORT erase_flash
esptool.py --port $PORT --baud 460800 write_flash --flash_size=detect 0 $BIN

