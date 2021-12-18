#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt update
apt install libsdl2-dev libgtkmm-3.0-dev libportaudio2 python3-gi libopenjp2-7 git ninja-build xorg python3-pip meson libjpeg-dev zlib1g-dev cmake extra-cmake-modules qttools5-dev qttools5-dev-tools libqt5x11extras5-dev libsdl2-dev libxi-dev libxtst-dev libx11-dev itstool gettext fbi -y

pip3 install pillow
pip3 install screeninfo

cp configFiles/gamepadmouse.gamecontroller.amgp /home/$SUDO_USER/gamepadmouse.gamecontroller.amgp

mkdir -p /opt/retro

cp configFiles/start.sh /home/$SUDO_USER

cp configFiles/usbManagement.sh /opt/retro

cp configFiles/rebootScreen.py /opt/retro

cp configFiles/newGame.glade /opt/retro

cp configFiles/splash.service /etc/systemd/system/

mkdir -p /usr/share/plymouth/themes/pix/

mkdir ConsoleGUI/newRoms

cp configFiles/bootImage.jpg /usr/share/plymouth/themes/pix/

cp configFiles/bootImage.jpg /opt/retro

chmod 755 /opt/retro/usbManagement.sh

chmod 755 /opt/retro/rebootScreen.py

mkdir -p /home/$SUDO_USER/.config/snes9x

mkdir -p /home/$SUDO_USER/.config/antimicrox

cp configFiles/snes9x.conf /home/$SUDO_USER/.config/snes9x/snes9x.conf

cp configFiles/antimicrox_settings.ini /home/$SUDO_USER/.config/antimicrox/antimicrox_settings.ini

chown -R $SUDO_USER:$SUDO_USER /home/$SUDO_USER/.config/

cd /home/$SUDO_USER

export GIT_SSL_NO_VERIFY=1

git clone https://github.com/snes9xgit/snes9x.git

cd snes9x

git submodule update --init --recursive

cd gtk

meson build --prefix=/usr --buildtype=release --strip

cd build

ninja

ninja install

echo KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="usb", RUN+="/opt/retro/usbManagement.sh" | sudo tee --append /etc/udev/rules.d/10-usb.rules

cd /home/$SUDO_USER

git clone https://github.com/AntiMicroX/antimicrox.git

cd antimicrox
mkdir -p build && cd build
cmake ..
cmake --build .

cat /lib/systemd/system/systemd-udevd.service | sed -e "s/PrivateMounts=yes/PrivateMounts=no/" > temp.txt

mv temp.txt /lib/systemd/system/systemd-udevd.service

echo "/home/pi/start.sh 2>/dev/null" >> /home/$SUDO_USER/.bashrc

cat /boot/cmdline.txt | sed -e "s/console=serial0,115200 console=tty1/console=tty0,115200 console=serial0/" > temp2.txt

mv temp2.txt /boot/cmdline.txt

echo "export count=1" >> /etc/profile

#systemctl enable splash

reboot
