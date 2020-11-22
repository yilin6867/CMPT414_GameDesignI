import pygame
from Gameworld import Gameworld

if __name__ == "__main__":
    world = Gameworld()
    while not world.game_over:
        world.run()
    pygame.quit()
