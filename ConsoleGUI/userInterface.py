#!/bin/python3
import gi
from resize import resize1
from resize import resize2
from resize import headerSize
from screeninfo import get_monitors
import os
from inputListener import listener
import threading
import re

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        os.system("snes9x-gtk roms/" + button.get_name() + ".sfc")

    def change_size(self, scroll):
        screen = get_monitors()[0]
        height = screen.height
        scroll.set_min_content_height(height-headerSize())
        #scale = 1080 / 790
        #scroll.set_min_content_height(height/scale)


def gamepadMouse():
    os.system("~/antimicrox/build/bin/antimicrox --hidden")

def snes_resolution():
    screen = get_monitors()[0]
    file = open("/home/pi/.config/snes9x/snes9x.conf", "r")
    replacement = ""

    for line in file:
       line = line.strip()
       changes = re.sub('MainHeight             = [0-9]+', 'MainHeight             = ' + str(screen.height), line)
       changes = re.sub('MainWidth              = [0-9]+', 'MainWidth              = ' + str(screen.width), changes)
       changes = re.sub('PreferencesHeight      = [0-9]+', 'PreferencesHeight      = ' + str(screen.height), changes)
       changes = re.sub('PreferencesWidth       = [0-9]+', 'PreferencesWidth       = ' + str(screen.width), changes)
       replacement = replacement + changes + "\n"

    file.close()

    fout = open("/home/pi/.config/snes9x/snes9x.conf", "w")
    fout.write(replacement)
    fout.close()

resize1('images/snes9x.jpg')

list = os.listdir("images")
list.remove("snes9x.jpg")

for images in list:
    resize2("images/"+images)


listen= threading.Thread(target=listener, args=())
listen.start()

game= threading.Thread(target=gamepadMouse, args=())
game.start()

snes_resolution()

builder = Gtk.Builder()
builder.add_from_file("userInterface.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
#window.fullscreen()
window.show_all()


Gtk.main()



