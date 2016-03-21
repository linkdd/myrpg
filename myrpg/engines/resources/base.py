# -*- coding: utf-8 -*-

from myrpg import PACKAGE

from xdg.BaseDirectory import xdg_data_home, xdg_data_dirs
import pkg_resources
import os


class Resource(object):

    resource_type = 'rsrc'

    class Error(Exception):
        pass

    def get_stream(self, name):
        rtype = self.__class__.resource_type

        dirs = [xdg_data_home] + xdg_data_dirs

        for datadir in dirs:
            rsrc = os.path.join(datadir, PACKAGE, rtype, name)

            if os.path.exists(rsrc):
                return open(rsrc)

        rsrc = os.path.join(rtype, name)
        if pkg_resources.resource_exists(rsrc):
            return pkg_resources.resource_stream(rsrc)

        raise Resource.Error('No resource found: type={0}, name={1}'.format(
            rtype, name
        ))

    def get_object(self, name, stream):
        return stream.read()

    def load(self, name):
        with self.get_stream(name) as stream:
            obj = self.get_object(name, stream)

        return obj
