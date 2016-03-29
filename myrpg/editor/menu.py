# -*- coding: utf-8 -*-

from myrpg.editor.dialog import ProjectDialog

from gi.repository import Gtk, GObject

import json
import os


class MenuBar(Gtk.MenuBar):

    __gsignals__ = {
        'project_loaded': (
            GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE,
            (
                GObject.TYPE_STRING,
                GObject.TYPE_STRING
            )
        )
    }

    def __init__(self, agr, parent=None, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)

        self.parent = parent

        filemenu = Gtk.Menu()
        filem = Gtk.MenuItem('&File')
        filem.set_submenu(filemenu)

        flags = Gtk.AccelFlags.VISIBLE

        newi = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_NEW, agr)
        key, mod = Gtk.accelerator_parse('<Control>N')
        newi.add_accelerator('activate', agr, key, mod, flags)
        newi.connect('activate', self.new_project)
        filemenu.append(newi)

        openi = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_OPEN, agr)
        key, mod = Gtk.accelerator_parse('<Control>O')
        openi.add_accelerator('activate', agr, key, mod, flags)
        openi.connect('activate', self.open_project)
        filemenu.append(openi)

        exiti = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, agr)
        key, mod = Gtk.accelerator_parse('<Control>Q')
        exiti.add_accelerator('activate', agr, key, mod, flags)
        exiti.connect('activate', Gtk.main_quit)
        filemenu.append(exiti)

        self.append(filem)

    def new_project(self, sender):
        project, ok = ProjectDialog.get_project_config(self.parent)

        if ok and project:
            if not os.path.exists(project['directory']):
                os.makedirs(project['directory'])

            project_dir = os.path.expanduser(project['directory'])
            project_path = os.path.join(
                project_dir,
                '{0}.json'.format(project['package'])
            )

            with open(project_path, 'w') as f:
                json.dump(project, f)

            for path in ['menus', 'objects', 'tilesets', 'maps']:
                fullpath = os.path.join(project_dir, path)

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

            self.emit(
                'project_loaded',
                project['package'],
                project['directory']
            )

    def open_project(self, sender):
        dialog = Gtk.FileChooserDialog(
            'Select project',
            self.parent,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK
            )
        )

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            project_path = dialog.get_filename()

            with open(project_path) as f:
                project = json.load(f)

            self.emit(
                'project_loaded',
                project['package'],
                project['directory']
            )

        dialog.destroy()
