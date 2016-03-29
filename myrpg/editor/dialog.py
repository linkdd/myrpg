# -*- coding: utf-8 -*-

from gi.repository import Gtk


class ProjectDialog(Gtk.Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(ProjectDialog, self).__init__(
            'Create new project',
            parent, 0,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK
            ),
            *args, **kwargs
        )

        layout = self.get_content_area()

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        lbl = Gtk.Label('Project name:')
        self.proj_name = Gtk.Entry()

        row.pack_start(lbl, False, True, 0)
        row.pack_start(self.proj_name, True, True, 0)

        layout.pack_start(row, True, True, 0)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        lbl = Gtk.Label('Project directory:')
        self.proj_dir = Gtk.Entry()
        btn = Gtk.Button('...', self)
        btn.connect('clicked', self.choose_dir)

        row.pack_start(lbl, False, True, 0)
        row.pack_start(self.proj_dir, True, True, 0)
        row.pack_end(btn, False, True, 0)

        layout.pack_start(row, True, True, 0)

        self.show_all()

    def choose_dir(self, sender):
        dialog = Gtk.FileChooserDialog(
            'Choose existing directory',
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK
            )
        )

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.proj_dir.set_text(dialog.get_filename())

        dialog.destroy()

    @staticmethod
    def get_project_config(parent=None):
        dialog = ProjectDialog(parent=parent)
        result = None, False

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            project = {
                'package': dialog.proj_name.get_text(),
                'directory': dialog.proj_dir.get_text()
            }

            result = project, True

        dialog.destroy()

        return result


class AddItemDialog(Gtk.Dialog):
    def __init__(self, itemname, parent=None, *args, **kwargs):
        super(AddItemDialog, self).__init__(
            'Create new {0}'.format(itemname),
            parent, 0,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK
            ),
            *args, **kwargs
        )

        layout = self.get_content_area()

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        lbl = Gtk.Label('Item name:')
        self.name = Gtk.Entry()

        row.pack_start(lbl, False, True, 0)
        row.pack_start(self.name, True, True, 0)

        layout.pack_start(row, True, True, 0)

        self.show_all()

    @staticmethod
    def get_item_name(itemname, parent=None):
        dialog = AddItemDialog(itemname, parent=parent)
        result = None

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            result = dialog.name.get_text()

        dialog.destroy()

        return result
