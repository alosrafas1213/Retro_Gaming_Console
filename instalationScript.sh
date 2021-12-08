#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt update
apt install libsdl2-dev libgtkmm-3.0-dev libportaudio2 python3-gi libopenjp2-7 git ninja-build xorg python3-pip meson libjpeg-dev zlib1g-dev cmake extra-cmake-modules qttools5-dev qttools5-dev-tools libsdl2-dev libxi-dev libxtst-dev libx11-dev itstool gettext -y

pip3 install pillow
pip3 install screeninfo

cp configFiles/gamepadmouse.gamecontroller.amgp ~/gamepadmouse.gamecontroller.amgp

mkdir -p /opt/retro

cp configFiles/start.sh ~/

cp configFiles/retro.service /etc/systemd/system/retro.service

chmod 644/etc/systemd/system/retro.service

cp configFiles/usbManagement.sh /opt/retro

chmod 755 /opt/retro/usbManagement.sh

mkdir -p ~/.config/snes9x

mkdir -p ~/.config/antimicrox

cp configFiles/snes9x.conf ~/.config/snes9x/snes9x.conf

cp configFiles/antimicrox_settings.ini ~/.config/antimicrox/antimicrox_settings.ini

chown -R $USER:$USER ~/.config/

cd

git clone https://github.com/snes9xgit/snes9x.git

cd snes9x

git submodule update --init --recursive

cd gtk

meson build --prefix=/usr --buildtype=release --strip

cd build

ninja

ninja install

echo KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="usb", RUN+="/opt/retro/usbManagement.sh" | sudo tee --append /etc/udev/rules.d/10-usb.rules

cd

git clone https://github.com/juliagoda/antimicroX.git

cd antimicrox
mkdir build && cd build
cmake ..
cmake --build .

cat /lib/systemd/system/systemd-udevd.service | sed -e "s/PrivateMounts=yes/PrivateMounts=no/" > temp.txt

mv temp.txt /lib/systemd/system/systemd-udevd.service

reboot
