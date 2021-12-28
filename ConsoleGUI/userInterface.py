#!/bin/python3
import gi
from resize import resize1
from resize import resize2
from resize import resizeNewImages
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
        os.system("snes9x-gtk " + '"roms/' + button.get_name() + '.sfc"')

    def change_size(self, scroll):
        screen = get_monitors()[0]
        height = screen.height
        scroll.set_min_content_height(height-headerSize())

class newButton(Gtk.Button):

    def onNewButtonPressed(self,button):
        os.system("snes9x-gtk " + '"newRoms/' + button.get_name() + '.sfc"')

    def createNewButton(self,buttonName):

        list = os.listdir("resizedNewImages")

        if buttonName+'Resized.png' not in list:
            img = Gtk.Image.new_from_file('resizedNewImages/genericResized.png')
        else:
            img = Gtk.Image.new_from_file('resizedNewImages/'+buttonName+'Resized.png')

        button = Gtk.Button(name=buttonName, label=buttonName)
        button.set_image(img)
        button.set_image_position(Gtk.PositionType(2))
        button.set_always_show_image(True)
        button.connect("clicked", self.onNewButtonPressed)
        return button

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

def addNewGames(grid):
    columnNum=0
    rowNum=3
    addRow=1
    list = os.listdir("newRoms")
    if len(list)==0:
        return
    for n in list:
        os.rename("newRoms/"+n,"newRoms/"+n.replace(" ",""))
    list = os.listdir("newRoms")

    buttonWidget = []
    buttons = []
    buttonNumber = 0
    for n in list:
        if len(n.split('.sfc'))>1:
            if addRow==1:
                grid.insert_row(rowNum)
                addRow=0
            buttonWidget.append(newButton())
            buttons.append(buttonWidget[buttonNumber].createNewButton(n.split('.sfc')[0]))
            grid.attach (buttons[buttonNumber], columnNum, rowNum,1, 1)
            columnNum+=1
            buttonNumber+=1
            if columnNum==5:
                columnNum=0
                rowNum+=1
                addRow=1


resize1('images/snes9x.jpg')

list = os.listdir("images")
list.remove("snes9x.jpg")

list2 = os.listdir("newImages")

for images in list:
    resize2("images/"+images)

if len(list2)>0:
    for images in list2:
        os.rename("newImages/"+images,"newImages/"+images.replace(" ",""))
    list2 = os.listdir("newRoms")
    for images in list2:
        resizeNewImages("newImages/"+images)

listen= threading.Thread(target=listener, args=())
listen.start()

game= threading.Thread(target=gamepadMouse, args=())
game.start()

snes_resolution()

builder = Gtk.Builder()
builder.add_from_file("userInterface.glade")
builder.connect_signals(Handler())

grid = builder.get_object("gamesGrid")

addNewGames(grid)



window = builder.get_object("window1")
#window.fullscreen()
window.show_all()


Gtk.main()



