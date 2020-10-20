import pygame

from DataModel.Entity.Entity import Entity

class atk_range_blk(Entity):
    def __init__(self, scrn, color, pos, chara):
        super().__init__(pos, chara.atkRange*2, "")
        self.screen = scrn
        self.src_chara = chara
        self.radius = chara.atkRange
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=self.pos)
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.dead = False


    def update(self):
        mouse_coords = pygame.mouse.get_pos()
        self.rect.x = mouse_coords[0] - self.radius
        self.rect.y = mouse_coords[1] - self.radius
