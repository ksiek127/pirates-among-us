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

    # def update_position(self, player):
    #     player_x, player_y = player.position
    #     player_w, player_h = player.image.get_rect().size
    #     self.x = player_x+player_w/2 - self.width/2
    #     self.y = player_y+player_h/2 - self.height/2

    def move(self):
        self.x_offset += self.x_change
        self.y_offset += self.y_change

    def unmove(self):
        self.x_offset -= self.x_change
        self.y_offset -= self.y_change

    # def update_position(self):
    #     self.rect.x += self.x_change
    #     self.rect.y += self.y_change
