#!/bin/bash

devicesList=`blkid | grep '/dev/sd' | cut -d ":" -f 1`
IFS=$'\n' read -rd '' -a devicearray <<<"$devicesList"

mountedDevices=`df -h | grep "/dev/sd" | cut -d " " -f 1`

IFS=$'\n' read -rd '' -a mountedArray <<<"$mountedDevices"

count=1
cond=0

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
        if [[ -d /media/usb$count/roms ]]
        then
            cp /media/usb$count/roms/*.sfc /home/pi/roms/
        fi
        count=$(( $count + 1 ))
    fi
done

