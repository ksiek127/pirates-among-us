import pygame

from objects.button import Button


class VotingButton(Button):
    def __init__(self, position, img, width, height, name, id):
        super().__init__(position, img, width, height)
        self.name = name
        self.id = id
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.textSurf = self.font.render(name, True, (255, 255, 255))
        w = self.textSurf.get_width()
        h = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - w / 2, height / 2 - h / 2])
