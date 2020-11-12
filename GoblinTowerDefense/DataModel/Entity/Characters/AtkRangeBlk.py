import pygame
import pygame.gfxdraw

from DataModel.Entity.Entity import Entity


class AtkRangeBlk(Entity):
    def __init__(self, scrn, color, pos, chara):
        super().__init__(pos, chara.atk_range * 2, "")
        self.screen = scrn
        self.src_chara = chara
        self.radius = chara.atk_range
        self.pos = pygame.math.Vector2()
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.pos)
        self.image.set_alpha(128)

    def update(self):
        mouse_coords = pygame.mouse.get_pos()
        self.rect.x = mouse_coords[0] - self.radius
        self.rect.y = mouse_coords[1] - self.radius
