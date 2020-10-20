import pygame
import math
from DataModel.Entity.Entity import Entity


class AttackBlock(Entity):
    rock="icons/attacks/rock.jpg"
    rock_spd = 5
    size=(10, 10)

    def __init__(self, scrn, pos, size, img_file, damage, target):
        super().__init__(pos, size, img_file)
        self.screen = scrn
        self.damage = damage
        self.speed = AttackBlock.rock_spd
        self.target = target
        self.landed = False

    def update(self):
        diff_x = self.target.rect.x - self.rect.x
        diff_y = self.target.rect.y - self.rect.y

        angle = math.atan2(diff_x, diff_y)
        next_x = self.speed * math.sin(angle)
        next_y = self.speed * math.cos(angle)

        if (self.rect.x > self.target.rect.x - self.speed
            and self.rect.x < self.target.rect.x + self.speed) and (
                self.rect.y > self.target.rect.y - self.speed
                and self.rect.y < self.target.rect.y + self.speed):
            self.rect.x = self.target.rect.x
            self.rect.y = self.target.rect.y
            self.landed = True
        else:
            self.rect.x = self.rect.x + math.floor(next_x)
            self.rect.y = self.rect.y + math.floor(next_y)