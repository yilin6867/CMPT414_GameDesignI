import pygame

from DataModel.Color import Color


class Entity(pygame.sprite.Sprite):

    def __init__(self, pos, size, renderImgFile):
        super().__init__()
        self.pos = pos
        self.size = size
        if len(renderImgFile) > 0:
            self.renderImgFile = renderImgFile
            self.image = pygame.image.load(self.renderImgFile).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.rect = self.image.get_rect(center=pygame.math.Vector2())
            self.radius = (self.size[0] / 2)
            self.rect.x = self.pos[0] - (self.size[0] / 2)
            self.rect.y = self.pos[1] - (self.size[1] / 2)
            #self.image.fill((255, 255, 255))
            pygame.draw.circle(self.image, Color.BLACK, (self.rect.x, self.rect.y), 10, True)

    def update(self):
        pass

    def render(self):
        pass
