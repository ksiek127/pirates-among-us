import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, filepath, width, height):
        super(Background, self).__init__()
        self.width = width
        self.height = height
        self.img = pygame.image.load(filepath)
        self.x = 0
        self.y = 0
        self.x_offset = -3100
        self.y_offset = -2000
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.x_change = 0
        self.y_change = 0

    def show(self, screen):
        screen.blit(self.img, (self.x + self.x_offset, self.y + self.y_offset))

    def move(self):
        self.x_offset += self.x_change
        self.y_offset += self.y_change

    def unmove(self):
        self.x_offset -= self.x_change
        self.y_offset -= self.y_change
