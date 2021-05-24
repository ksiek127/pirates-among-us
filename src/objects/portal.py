import pygame
from objects.map_object import MapObject


class Portal(MapObject):
    def __init__(self, position, width, height, radius, where_teleports):
        super().__init__(position, width, height, radius)
        self.where_teleports = where_teleports
