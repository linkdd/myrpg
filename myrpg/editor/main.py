# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from myrpg.editor.win import MainWindow

import sys


def main():
    Gtk.init(sys.argv)

    win = MainWindow()
    win.show_all()

    Gtk.main()
