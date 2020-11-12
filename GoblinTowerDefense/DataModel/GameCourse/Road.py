import pygame


class Road(pygame.sprite.Sprite):
    def __init__(self, color, coords):
        super().__init__()

        # Fetch the rectangle object that has the dimensions of the image
        self.image = pygame.Surface((coords[2], coords[3]))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
