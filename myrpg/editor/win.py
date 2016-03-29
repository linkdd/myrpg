# -*- coding: utf-8 -*-

from gi.repository import Gtk

from myrpg.editor.menu import MenuBar
from myrpg.editor.view import View


class MainWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        agr = Gtk.AccelGroup()
        self.add_accel_group(agr)

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.menubar = MenuBar(agr, parent=self)
        self.view = View(agr, parent=self)

        layout.pack_start(self.menubar, False, True, 0)
        layout.pack_start(self.view, True, True, 0)

        self.add(layout)

        self.connect('delete_event', Gtk.main_quit)
        self.menubar.connect('project_loaded', self.view.load_project)
