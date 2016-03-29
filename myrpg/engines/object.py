# -*- coding: utf-8 -*-

from myrpg.resources.object import ObjectResource
from lupa import LuaRuntime


class ObjectInstance(object):
    def __init__(self, name, definition, sprites, *args, **kwargs):
        super(ObjectInstance, self).__init__(*args, **kwargs)

        self.type = name
        self.data = definition
        self.sprites = sprites
        self.sprite = None

    def delete(self):
        pass

    def set_sprite(self, name):
        self.sprite = self.sprites[name]


class ObjectWrapper(object):
    def __init__(self, name, *args, **kwargs):
        super(ObjectWrapper, self).__init__(*args, **kwargs)

        rsrc = ObjectResource().load(name)

        self.instance = ObjectInstance(name, rsrc[0], rsrc[1])
        self.lua = LuaRuntime()
        self.lua.execute(rsrc[2])

    def __getattr__(self, attr):
        if attr.startswith('lua_'):
            return self.lua.globals().get(attr)

    def create(self):
        if self.lua_create is not None:
            self.lua_create(self.instance)

    def destroy(self):
        if self.lua_destroy is not None:
            self.lua_destroy(self.instance)

    def mouseenter(self):
        if self.lua_mouseenter is not None:
            self.lua_mouseenter(self.instance)

    def mouseleave(self):
        if self.lua_mouseleave is not None:
            self.lua_mouseleave(self.instance)

    def keypress(self, key, modifier):
        if self.lua_keypress is not None:
            self.lua_keypress(self.instance, key, modifier)

    def keyrelease(self, key, modifier):
        if self.lua_keyrelease is not None:
            self.lua_keyrelease(self.instance, key, modifier)

    def draw(self):
        if self.lua_draw is not None:
            self.lua_draw(self.instance)

    def collision(self, other):
        if self.lua_collision is not None:
            self.lua_collision(self.instance, self.other)
