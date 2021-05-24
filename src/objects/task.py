import pygame

from objects.map_object import MapObject


class Task(MapObject):
    def __init__(self, position, width, height, radius, task_type):
        super().__init__(position, width, height, radius)
        self.x = 0
        self.y = 0
        self.x_offset = position[0]
        self.y_offset = position[1]
        self.rect = pygame.Rect(position, (self.width, self.height))
        self.x_change = 0
        self.y_change = 0
        self.duration = 5

        self.task_type = task_type
        self.position = position  # glowny punkt
