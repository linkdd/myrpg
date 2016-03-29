# -*- coding: utf-8 -*-

from gi.repository import Gtk

from myrpg.editor.tree import ProjectTree
from myrpg.editor.workspace import ProjectWorkspace


class View(Gtk.HPaned):
    def __init__(self, agr, parent=None, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.tree = ProjectTree(parent=parent)
        self.workspace = ProjectWorkspace()

        self.pack1(self.tree, True, True)
        self.pack2(self.workspace, True, False)

    def load_project(self, sender, package, directory):
        project = {
            'package': package,
            'directory': directory
        }

        self.tree.load_project(project)
