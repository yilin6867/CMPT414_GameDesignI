import math
import pygame
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock
from DataModel.Entity.Entity import Entity


class Character(Entity):
    size = (50, 50)
    swordman_img_file = "icons/characters/GoblinSlayer.png"
    archer_img_file = "icons/characters/archer.png"
    priest_img_file = "icons/characters/priest.png"
    wizard_img_file = "icons/characters/widzard.png"
    img_files=[swordman_img_file]

    def __init__(self, scrn, upgrade_cost, level, atkPoint, atk_range, atk_cd, renderImgFile, atk_img_file):
        super().__init__(pygame.mouse.get_pos(), Character.size, renderImgFile)
        self.upgrade_cost = upgrade_cost
        self.level = level
        self.atk_point = atkPoint
        self.def_atk_cd = atk_cd
        self.atk_cd = 0
        self.atkRange = atk_range
        self.atk_img_file = atk_img_file
        self.screen = scrn
        self.dragable = True

    def render(self):
        pass

    def update(self):
        mouse_coords = pygame.mouse.get_pos()
        self.rect.x = mouse_coords[0] - self.size[0]
        self.rect.y = mouse_coords[1] - self.size[1]

    def attack(self, enemy):
        if (self.atk_cd == 0):
            self.atk_cd = self.def_atk_cd
            attack_coords = [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2]
            return AttackBlock(self.screen, attack_coords, AttackBlock.size, self.atk_img_file, self.atk_point, enemy)
        else:
            self.atk_cd = self.atk_cd - 1
            return None