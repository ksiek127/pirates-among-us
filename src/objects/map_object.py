import pygame


class MapObject(pygame.sprite.Sprite):
    def __init__(self, position, width, height, radius):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.x_offset = position[0]
        self.y_offset = position[1]
        self.rect = pygame.Rect(position, (self.width, self.height))
        self.radius = radius
        self.position = position  # glowny punkt

    def is_near(self, position):
        position_diff = [self.position[0] - position[0],
                         self.position[1] - position[1]]
        if abs(position_diff[0]) <= self.radius and abs(position_diff[1]) <= self.radius:
            return True
        else:
            return False

    def show(self, screen, img, where):
        screen.blit(img, where)
