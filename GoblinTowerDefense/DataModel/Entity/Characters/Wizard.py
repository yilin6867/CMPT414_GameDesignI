import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class Wizard(Character):
    init_level = 1
    init_upgrade_cost = 5 * (init_level ** 3) / 4
    init_atk = 10
    init_atk_range = 150
    attack_growth = 1.4
    attack_cd = 50

    def __init__(self, scrn):
        super().__init__(scrn,
                         Wizard.init_upgrade_cost,
                         Wizard.init_level,
                         Wizard.init_atk,
                         Wizard.init_atk_range,
                         Wizard.attack_cd,
                         AttackBlock.fireball_spd,
                         Character.wizard_img_file,
                         AttackBlock.fireball
                         )
        self.atkPoint = Wizard.init_atk + (self.level * 1.3)

    def level_up(self):
        # Section to implement level up
        if self.upgrade_cost <= 0:
            self.level = self.level + 1
            self.atk_point = Wizard.init_atk + (self.level * 1.3)
            self.upgrade_cost = self.get_upgrade_cost()

    def get_upgrade_cost(self):
        return 5 * (self.level ** 3) / 4

    def attack(self, enemy):
        if self.atk_cd == 0:
            self.atk_cd = self.def_atk_cd
            attack_coords = [self.rect.x + self.size[0] // 2,
                             self.rect.y + self.size[1] // 2]
            return AttackBlock(self.screen, attack_coords, AttackBlock.size,
                               self.atk_img_file, self.atk_point,
                               self.atk_spd, True, enemy, self, "")
        else:
            self.atk_cd = self.atk_cd - 1
            return None
