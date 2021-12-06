#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt install libsdl2-dev libgtkmm-3.0-dev libportaudio2 python3-gi libopenjp2-7 git ninja-build xorg python3-pip meson -y

git clone https://github.com/snes9xgit/snes9x.git

cd snes9x/gtk

meson build --prefix=/usr --buildtype=release --strip

cd build

ninja

ninja install
