# -*- coding: utf-8 -*-

from myrpg.engines.resources.map import MapResource
from myrpg.engines.tile.objects import ObjectGroup
from myrpg.engines.tile.layer import Layer


class Map(object):
    @property
    def width(self):
        return self.data['width']

    @property
    def height(self):
        return self.data['height']

    @property
    def tilewidth(self):
        return self.data['tilewidth']

    @property
    def tileheight(self):
        return self.data['tileheight']

    def __init__(self, name, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)

        self.data = MapResource().load(name)
        self.layers = map(Layer, self.data['layers'])
        self.objects = map(ObjectGroup, self.data['objectgroups'])
