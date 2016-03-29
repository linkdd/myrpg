# -*- coding: utf-8 -*-

from myrpg.engines.tileset import Tileset


class Layer(object):
    @property
    def level(self):
        return self.data['level']

    def __init__(self, data, *args, **kwargs):
        super(Layer, self).__init__(*args, **kwargs)

        self.data = data
        self.tileset = Tileset(self.data['tileset'])

    def __getitem__(self, index):
        x, y = index

        return self.data['data'][x][y]
