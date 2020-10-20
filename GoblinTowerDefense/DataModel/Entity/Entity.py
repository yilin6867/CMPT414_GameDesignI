import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, size, renderImgFile):
        super().__init__()
        self.pos = pos
        self.size = size
        if (len(renderImgFile) > 0) :
            self.renderImgFile = renderImgFile
            self.image = pygame.image.load(self.renderImgFile)
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.rect = self.image.get_rect()
            self.rect.x = self.pos[0] - (self.size[0] / 2)
            self.rect.y = self.pos[1] - (self.size[1] / 2)

    def update(self):
        pass

    def render(self):
        pass