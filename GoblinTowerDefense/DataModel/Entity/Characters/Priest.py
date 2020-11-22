import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class Priest(Character):
    init_level = 1
    init_upgrade_cost = (4 * (init_level ** 3)) / 5
    init_atk = 1
    init_atk_range = 75
    attack_growth = 1.1
    attack_cd = 40

    def __init__(self, scrn):
        super().__init__(scrn,
                         Priest.init_upgrade_cost,
                         Priest.init_level,
                         Priest.init_atk,
                         Priest.init_atk_range,
                         Priest.attack_cd,
                         AttackBlock.holylight_spd,
                         Character.priest_img_file,
                         AttackBlock.holy_light
                         )
        self.atkPoint = Priest.init_atk + (self.level * 1.3)

    def level_up(self):
        # Section to implement level up
        if self.upgrade_cost <= 0:
            self.level = self.level + 1
            self.atk_point = Priest.init_atk + (self.level * 1.3)
            self.upgrade_cost = self.get_upgrade_cost()

    def get_upgrade_cost(self):
        return (4 * (self.level ** 3)) / 5

    def attack(self, enemy):
        if self.atk_cd == 0:
            self.atk_cd = self.def_atk_cd
            attack_coords = [self.rect.x + self.size[0] // 2,
                             self.rect.y + self.size[1] // 2]
            effect = "slow"
            return AttackBlock(self.screen, attack_coords, AttackBlock.size,
                               self.atk_img_file, self.atk_point,
                               self.atk_spd, False, enemy, self, effect)
        else:
            self.atk_cd = self.atk_cd - 1
            return None
