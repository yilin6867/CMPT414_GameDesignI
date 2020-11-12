import pygame
from DataModel.Entity.Entity import Entity
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class Character(Entity):
    size = (50, 50)
    goblinslayer_img_file = "Ext/characters/GoblinSlayer.png"
    archer_img_file = "Ext/characters/archer.png"
    priest_img_file = "Ext/characters/priest.png"
    wizard_img_file = "Ext/characters/widzard.png"
    img_files = [goblinslayer_img_file, archer_img_file, priest_img_file, wizard_img_file]

    def __init__(self, scrn, upgrade_cost, level, atkPoint, atk_range, atk_cd, atk_spd, renderImgFile, atk_img_file):
        super().__init__(pygame.mouse.get_pos(), Character.size, renderImgFile)
        self.upgrade_cost = upgrade_cost
        self.level = level
        self.atk_point = atkPoint
        self.def_atk_cd = atk_cd
        self.atk_cd = 0
        self.atk_spd = atk_spd
        self.atk_range = atk_range
        self.atk_img_file = atk_img_file
        self.screen = scrn
        self.draggable = True
        self.atk_range_blk = None

    def update(self):
        # Allow character to be move around before being place on a location
        if self.draggable:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = mouse_pos[0] - self.size[0] // 2
            self.rect.y = mouse_pos[1] - self.size[0] // 2
        self.level_up()

    def clicked(self, mouse_pos):
        if (mouse_pos[0] >= self.rect.x and mouse_pos[0] <= self.rect.x + self.size[0]) and (
                mouse_pos[1] >= self.rect.y and mouse_pos[1] <= self.rect.y + self.size[1]):
            return self
        else:
            return None

    def attack(self, enemy):
        if self.atk_cd == 0:
            self.atk_cd = self.def_atk_cd
            attack_coords = [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2]
            attack_block = AttackBlock(self.screen, attack_coords, AttackBlock.size, self.atk_img_file, self.atk_point,
                                       self.atk_spd, False, enemy, self, "")
            if (attack_block.target_x > self.rect.x and attack_block.target_y < self.rect.y):
                attack_block.rotate(0)
            elif (attack_block.target_x < self.rect.x and attack_block.target_y > self.rect.y):
                attack_block.rotate(180)
            elif (attack_block.target_x > self.rect.x and attack_block.target_y > self.rect.y):
                attack_block.rotate(270)
            elif (attack_block.target_x < self.rect.x and attack_block.target_y < self.rect.y):
                attack_block.rotate(90)
            return attack_block
        else:
            self.atk_cd = self.atk_cd - 1
            return None
