import gi
from resize import resize1
from resize import resize2
from resize import headerSize
from screeninfo import get_monitors
from pynput import keyboard
import os

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
        #scroll.set_min_content_height(height-headerSize())
        scale = 1080 / 790
        scroll.set_min_content_height(height/scale-10)

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

resize1('images/snes9x.jpg')

list = os.listdir("images")
list.remove("snes9x.jpg")

for images in list:
    resize2("images/"+images)

builder = Gtk.Builder()
builder.add_from_file("test.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
#window.fullscreen()
window.show_all()

Gtk.main()


#listener.join()  # remove if main thread is polling self.keys

