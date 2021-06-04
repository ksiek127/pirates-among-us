import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, position, img, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.width = width
        self.height = height
        self.image = pygame.image.load(img)
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def pressed(self, mouse):
        return self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
               self.rect.bottomright[1]
