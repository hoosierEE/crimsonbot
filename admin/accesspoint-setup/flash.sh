#! /bin/sh

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "Must include a root folder for upload files"

IMG="esp8266-20170612-v1.9.1.bin"
FILES="crimsonbot.py net_cfg.py webrepl_cfg.py cb_setup.py esp_setup.py boot.py main.py"

esptool.py -p /dev/ttyUSB0 erase_flash
echo "-----FLASHING $IMG----"
esptool.py -p /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 $IMG
echo -n "-----WAITING FOR RESET"
for _ in {1..5}
do
    echo -n "."
    sleep 1
done
echo -e "\n"
for f in $FILES
do
    echo "----FLASHING $f-----"
    ampy -p /dev/ttyUSB0 put "$1/$f"
done

echo -e "\nCreating inventory..."
python add_to_inv.py
