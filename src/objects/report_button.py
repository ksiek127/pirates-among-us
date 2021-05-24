import pygame

from objects.map_object import MapObject


class ReportButton(MapObject):
    def __init__(self, position, width, height, radius):
        super().__init__(position, width, height, radius)
        self.x = 0
        self.y = 0
        self.x_offset = position[0]
        self.y_offset = position[1]
        self.x_change = 0
        self.y_change = 0

        self.radius = radius
        self.position = position  # glowny punkt
