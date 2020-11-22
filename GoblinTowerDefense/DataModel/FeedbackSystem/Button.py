import pygame
from DataModel.Color import Color
from DataModel.Entity.Entity import Entity


class Button(Entity):
    def __init__(self, pos, size, text):
        super().__init__(pos, size, "")
        self.image = pygame.Surface(size)
        self.image.set_alpha(255)
        self.image.fill(Color.GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.render_text = text
        self.text_blk = self.image.blit(self.render_text, [0, 0])
        self.on = False

    def click(self, click_pos):
        if ((click_pos[0] > self.rect.x) and
            (click_pos[0] < self.rect.x + self.size[0])) and (
                (click_pos[1] > self.rect.y) and
                (click_pos[1] < self.rect.y + self.size[1])):
            self.image.fill(Color.GRAY if self.on else Color.RED)
            self.image.blit(self.render_text, [0, 0])
            self.on = False if self.on else True
            return True
        else:
            return False
