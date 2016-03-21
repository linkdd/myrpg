# -*- coding: utf-8 -*-

from myrpg.engines.resources.tileset import TilesetResource
from pyglet import gl
import pyglet


class Tileset(object):

    class Error(Exception):
        pass

    @property
    def width(self):
        return self.definition['tileset']['width']

    @property
    def height(self):
        return self.definition['tileset']['height']

    def __init__(self, name, *args, **kwargs):
        super(Tileset, self).__init__(*args, **kwargs)

        rsrc = TilesetResource().load(name)

        self.definition = rsrc[0]
        self.image = rsrc[1]

        margin = self.definition['tileset']['margin']
        spacing = self.definition['tileset']['spacing']

        self.region = self.image.get_region(
            margin,
            margin,
            self.image.width - margin * 2,
            self.image.height - margin * 2
        )
        self.grid = pyglet.image.ImageGrid(
            self.region,
            self.region.height // self.height,
            self.region.width // self.width,
            row_padding=spacing,
            column_padding=spacing
        )

        self.texture = self.grid.get_texture_sequence()

        if self.definition['tileset']['nearest']:
            gl.glTextParameteri(
                self.texture.target,
                gl.GL_TEXTURE_MIN_FILTER,
                gl.GL_NEAREST
            )
            gl.glTextParameteri(
                self.texture.target,
                gl.GL_TEXTURE_MAG_FILTER,
                gl.GL_NEAREST
            )

    def __getitem__(self, name):
        index = self.definition['tiles'].get(name)

        if index is None:
            raise Tileset.Error('Unknown tile: {0}'.format(name))

        return self.texture[tuple(index)]
