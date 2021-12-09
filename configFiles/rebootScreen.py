#!/bin/python3
import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_rebootButton_clicked(self, button):
        os.system("sudo reboo")

    def on_acceptButton_clicked(self, button):
        Gtk.main_quit()

builder = Gtk.Builder()
builder.add_from_file("newGame.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
#window.fullscreen()
window.show_all()


Gtk.main()



