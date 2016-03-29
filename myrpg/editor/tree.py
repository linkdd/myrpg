# -*- coding: utf-8 -*-

from myrpg.editor.dialog import AddItemDialog

from gi.repository import Gtk

import shutil
import json
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

    def empty_nodes(self):
        model = self.get_model()

        for parent in [self.menus, self.objects, self.tilesets, self.maps]:
            if model.iter_has_child(parent):
                iterator = model.iter_children(parent)

                while iterator is not None:
                    model.remove(iterator)
                    iterator = model.iter_children(parent)

    def load_project(self, project):
        self.empty_nodes()

        self.project = project

        directories = {
            'menu': os.path.join(project['directory'], 'menus'),
            'object': os.path.join(project['directory'], 'objects'),
            'tileset': os.path.join(project['directory'], 'tilesets'),
            'map': os.path.join(project['directory'], 'maps')
        }

        for itemtype in directories:
            path = directories[itemtype]

            for name in os.listdir(path):
                self.load_item(itemtype, name)

    def load_item(self, itemtype, name):
        itemmap = {
            'menu': (self.menus, Gtk.STOCK_INDEX),
            'object': (self.objects, Gtk.STOCK_EXECUTE),
            'tileset': (self.tilesets, Gtk.STOCK_SELECT_COLOR),
            'map': (self.maps, Gtk.STOCK_PAGE_SETUP)
        }

        model = self.get_model()

        itemmodel = itemmap[itemtype]
        model.append(itemmodel[0], [itemmodel[1], name, itemtype])
        self.expand_all()

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
        if self.project is not None:
            itemname, _ = item

            newitemtype = itemname[:-1]
            newitem = AddItemDialog.get_item_name(
                newitemtype,
                parent=self.parentwin
            )

            handler = getattr(self, 'add_{0}'.format(newitemtype))
            handler(newitem)

            self.load_item(newitemtype, newitem)

        else:
            dialog = Gtk.MessageDialog(
                self.parentwin, 0,
                Gtk.MessageType.ERROR,
                (
                    Gtk.STOCK_OK, Gtk.ResponseType.OK
                ),
                'Impossible to create new item, no project loaded'
            )

            dialog.run()
            dialog.destroy()

    def delete_item(self, parent, item):
        itemname, itemtype = item

        model = self.get_model()

        for i in range(model.iter_n_children(parent)):
            child = model.iter_nth_child(parent, i)

            name = model.get_value(child, 1)

            if name == itemname:
                break

        else:
            child = None

        if child is not None:
            model.remove(child)

        itemtype = '{0}s'.format(itemtype)
        shutil.rmtree(
            os.path.join(self.project['directory'], itemtype, itemname)
        )

    def add_menu(self, item):
        itempath = os.path.join(self.project['directory'], 'menus', item)

        if not os.path.exists(itempath):
            os.makedirs(itempath)

            with open(os.path.join(itempath, 'definition.json'), 'w') as f:
                json.dump({'title': item, 'actions': []}, f)

            with open(os.path.join(itempath, 'script.lua'), 'w') as f:
                pass

    def edit_menu(self, widget, item):
        pass

    def delete_menu(self, widget, item):
        self.delete_item(self.menus, item)

    def add_object(self, item):
        itempath = os.path.join(self.project['directory'], 'objects', item)

        if not os.path.exists(itempath):
            os.makedirs(itempath)

            with open(os.path.join(itempath, 'definition.json'), 'w') as f:
                json.dump({}, f)

            with open(os.path.join(itempath, 'script.lua'), 'w') as f:
                pass

    def edit_object(self, widget, item):
        pass

    def delete_object(self, widget, item):
        self.delete_item(self.objects, item)

    def add_tileset(self, item):
        itempath = os.path.join(self.project['directory'], 'tilesets', item)

        if not os.path.exists(itempath):
            os.makedirs(itempath)

            with open(os.path.join(itempath, 'definition.json'), 'w') as f:
                json.dump({}, f)

            with open(os.path.join(itempath, 'tileset.png'), 'w') as f:
                pass

    def edit_tileset(self, widget, item):
        pass

    def delete_tileset(self, widget, item):
        self.delete_item(self.tilesets, item)

    def add_map(self, item):
        itempath = os.path.join(self.project['directory'], 'maps', item)

        if not os.path.exists(itempath):
            os.makedirs(itempath)

            with open(os.path.join(itempath, 'definition.json'), 'w') as f:
                json.dump({
                    'width': 0,
                    'height': 0,
                    'tilewidth': 16,
                    'tileheight': 16,
                    'layers': [],
                    'objectgroups': []
                }, f)

    def edit_map(self, widget, item):
        pass

    def delete_map(self, widget, item):
        self.delete_item(self.maps, item)
