# -*- coding: utf-8 -*-

from myrpg.resources.base import Resource
import pyglet
import json
import os


class TilesetResource(Resource):
    def get_object(self, name, stream, otype=None):
        if otype == 'def':
            return json.load(stream)

        elif otype == 'img':
            return pyglet.image.load(name, file=stream)

    def load(self, name):
        definition = os.path.join(name, 'definition.json')
        image = os.path.join(name, 'tileset.png')

        with self.get_stream(definition) as stream:
            definition = self.get_object(definition, stream, otype='def')

        with self.get_stream(image) as stream:
            image = self.get_object(image, stream, otype='img')

        return definition, image
