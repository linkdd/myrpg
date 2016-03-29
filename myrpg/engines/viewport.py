# -*- coding: utf-8 -*-

import pyglet


class Viewport(object):
    def __init__(self, map, w, h, *args, **kwargs):
        super(Viewport, self).__init__(*args, **kwargs)

        self.map = map

        self.batch = pyglet.graphics.Batch()

        self.w = w
        self.h = h

        self.sprites = {}
        self.groups = {
            layer.level: pyglet.graphics.OrderedGroup(layer.level)
            for layer in self.map
        }

    def _load_tile(self, layer, tilename, tx, ty, x, y):
        key = layer.level, tx, ty

        if key not in self.sprites:
            if tilename is None:
                self.sprites[key] = None

            else:
                texture = layer.tileset[tilename]
                self.sprites[key] = pyglet.sprite.Sprite(
                    texture,
                    x=(tx - x) * layer.tileset.width,
                    y=(ty - y) * layer.tileset.height,
                    batch=self.batch,
                    group=self.groups[layer.level]
                )

        return key

    def _update(self, x, y):
        use = []

        for layer in self.map:
            use += map(
                lambda tile: self._load_tile(
                    layer,
                    tile,
                    i, j,
                    x, y
                ),
                [
                    layer[i, j]
                    for i in range(x, self.w)
                    for j in range(y, self.h)
                ]
            )

        for key in self.sprites.keys():
            if key not in use:
                if self.sprites[key] is not None:
                    self.sprites[key].delete()

                del self.sprites[key]

    def focus(self, x, y):
        tx = x // self.map.tilewidth
        ty = y // self.map.tileheight

        vx = max(tx - self.w // 2, 0)
        vy = max(ty - self.h // 2, 0)

        if vx + self.w // 2 > self.map.width:
            vx = self.map.width - self.w

        if vy + self.h // 2 > self.map.height:
            vy = self.map.height - self.h

        self._update(vx, vy)

    def draw(self):
        self.batch.draw()
