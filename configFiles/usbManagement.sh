#!/bin/bash

sleep 5

devicesList=`blkid | grep '/dev/sd' | cut -d ":" -f 1`
IFS=$'\n' read -rd '' -a devicearray <<<"$devicesList"

mountedDevices=`df -h | grep "/dev/sd" | cut -d " " -f 1`

IFS=$'\n' read -rd '' -a mountedArray <<<"$mountedDevices"

cond=0
filesnum=0

for i in "${devicearray[@]}"; do
    for j in "${mountedArray[@]}"; do
        if [ "$i" = "$j" ]; then
            cond=1
        fi
    done
    if [ "$cond" -eq "1" ]; then
        cond=0
    else
        echo se monta $i >> /home/pi/testo.txt
        mkdir -p /media/usb$count
        mount $i /media/usb$count
        sleep 5
        if [[ -d /media/usb$count/roms ]]
        then
            files=`ls /media/usb$count/roms/*.sfc | wc -l`
            filesnum=$(( $filesnum + $files ))
            cp /media/usb$count/roms/*.sfc /home/pi/Retro_Gaming_Console/ConsoleGUI/newRoms/
        fi

        if [[ -d /media/usb$count/covers ]]
        then
            cp /media/usb$count/covers/*.png /home/pi/Retro_Gaming_Console/ConsoleGUI/newImages/
        fi
        count=$(( $count + 1 ))
    fi
done

chown -R pi:pi /home/pi/Retro_Gaming_Console/ConsoleGUI/newRoms/
chown -R pi:pi /home/pi/Retro_Gaming_Console/ConsoleGUI/newImages/

if [[ "$filesnum" -gt "0" ]]
then
    export DISPLAY=:0
    /opt/retro/rebootScreen.py
fi
