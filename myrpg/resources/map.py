# -*- coding: utf-8 -*-

from myrpg.resources.base import Resource
import json


class MapResource(Resource):

    resource_type = 'maps'

    def get_object(self, name, stream):
        return json.load(stream)

    def load(self, name):
        return super(MapResource, self).load('{0}.json'.format(name))
