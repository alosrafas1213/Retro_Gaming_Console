#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt install libsdl2-dev libgtkmm-3.0-dev libportaudio2 python3-gi libopenjp2-7 git ninja-build xorg python3-pip meson libjpeg-dev zlib1g-dev -y

pip3 install pillow
pip3 install screeninfo

git clone https://github.com/snes9xgit/snes9x.git

cd snes9x

git submodule update --init --recursive

cd gtk

meson build --prefix=/usr --buildtype=release --strip

cd build

ninja

ninja install

mkdir /media/usb

mkdir /opt/retro

cp usbManagement.sh /opt/retro

chmod 766 /opt/retro/usbManagement.sh

echo KERNEL=="sd?1", ATTRS{idVendor}=="*", ATTRS{idProduct}=="*", ATTRS{serial}=="*", SYMLINK+="usb", RUN+="/opt/retro/usbManagement.sh" | sudo tee --append /etc/udev/rules.d/81-thumbdrive.rules
