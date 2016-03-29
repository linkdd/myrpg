# -*- coding: utf-8 -*-

from gi.repository import Gtk


class ProjectWorkspace(Gtk.Notebook):
    def __init__(self, *args, **kwargs):
        super(ProjectWorkspace, self).__init__(*args, **kwargs)
