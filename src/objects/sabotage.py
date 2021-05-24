import pygame


class Sabotage:
    def __init__(self, cooldown):
        self.cooldown = cooldown

    def is_ready(self):
        return self.cooldown == 0

    def lights(self):
        pass

    def oxygen(self):
        pass

    def reactor(self):
        pass
