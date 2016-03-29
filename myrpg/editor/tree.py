# -*- coding: utf-8 -*-

from myrpg.editor.dialog import AddItemDialog

from gi.repository import Gtk

import os


class ProjectTree(Gtk.TreeView):
    def __init__(self, parent=None, *args, **kwargs):
        super(ProjectTree, self).__init__(*args, **kwargs)

        self.parentwin = parent
        self.project = None

        # create tree data
        model = Gtk.TreeStore(str, str, str)

        self.menus = model.append(
            None,
            [Gtk.STOCK_DIRECTORY, 'menus', 'category']
        )
        self.objects = model.append(
            None,
            [Gtk.STOCK_DIRECTORY, 'objects', 'category']
        )
        self.tilesets = model.append(
            None,
            [Gtk.STOCK_DIRECTORY, 'tilesets', 'category']
        )
        self.maps = model.append(
            None,
            [Gtk.STOCK_DIRECTORY, 'maps', 'category']
        )

        self.set_model(model)

        # create renderers
        renderer = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn('Icon', renderer, icon_name=0)
        self.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=1)
        self.append_column(column)

        # create contextual menus
        self.connect('button-press-event', self.on_button_press)

        self.contextual_menus = {
            'category': [
                (Gtk.STOCK_ADD, self.add_item)
            ],
            'menu': [
                (Gtk.STOCK_EDIT, self.edit_menu),
                (Gtk.STOCK_DELETE, self.delete_menu)
            ],
            'object': [
                (Gtk.STOCK_EDIT, self.edit_object),
                (Gtk.STOCK_DELETE, self.delete_object)
            ],
            'tileset': [
                (Gtk.STOCK_EDIT, self.edit_tileset),
                (Gtk.STOCK_DELETE, self.delete_tileset)
            ],
            'map': [
                (Gtk.STOCK_EDIT, self.edit_map),
                (Gtk.STOCK_DELETE, self.delete_map)
            ]
        }
        self.menus_cache = {}

    def get_context_menu(self, key, data):
        definition = self.contextual_menus[key]

        menu = Gtk.Menu()
        menu.context = None

        for icon, handler in definition:
            item = Gtk.ImageMenuItem.new_from_stock(icon, None)
            item.connect('activate', handler, data)
            menu.append(item)

        return menu

    def load_project(self, project):
        self.project = project

        menuspath = os.path.join(project['directory'], 'menus')
        objectspath = os.path.join(project['directory'], 'objects')
        tilesetspath = os.path.join(project['directory'], 'tilesets')
        mapspath = os.path.join(project['directory'], 'maps')

        model = self.get_model()

        for parent, path, icon, itemtype in [
            (self.menus, menuspath, Gtk.STOCK_INDEX, 'menu'),
            (self.objects, objectspath, Gtk.STOCK_EXECUTE, 'object'),
            (self.tilesets, tilesetspath, Gtk.STOCK_SELECT_COLOR, 'tileset'),
            (self.maps, mapspath, Gtk.STOCK_PAGE_SETUP, 'map')
        ]:
            for name in os.listdir(path):
                model.append(parent, [icon, name, itemtype])

    def on_button_press(self, widget, event):
        if event.button == 3:
            result = self.get_path_at_pos(int(event.x), int(event.y))

            if result is not None:
                model = self.get_model()
                path = result[0]
                iterator = model.get_iter(path)
                itemname = model.get_value(iterator, 1)
                itemtype = model.get_value(iterator, 2)

                data = (itemname, itemtype)

                if data not in self.menus_cache:
                    self.menus_cache[data] = self.get_context_menu(
                        itemtype, data
                    )

                menu = self.menus_cache[data]
                menu.show_all()
                menu.popup(None, None, None, None, event.button, event.time)

    def add_item(self, widget, item):
        itemname, itemtype = item

        newitem = AddItemDialog.get_item_name(
            itemname[:-1],
            parent=self.parentwin
        )

        print(itemname, itemtype, newitem)

    def edit_menu(self, widget, item):
        pass

    def delete_menu(self, widget, item):
        pass

    def edit_object(self, widget, item):
        pass

    def delete_object(self, widget, item):
        pass

    def edit_tileset(self, widget, item):
        pass

    def delete_tileset(self, widget, item):
        pass

    def edit_map(self, widget, item):
        pass

    def delete_map(self, widget, item):
        pass
