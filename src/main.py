import pygame
from game_state import GameState


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("AMONGUS3")
    game_st = GameState('menu')
    players = pygame.sprite.Group()
    game_st.state_manager()
