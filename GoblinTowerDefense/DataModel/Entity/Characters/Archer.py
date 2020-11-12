import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock

class Archer(Character):
    init_level = 1
    init_upgrade_cost = (4 * (init_level ** 3)) / 5
    init_atk = 3
    init_atk_range = 200
    attack_growth = 1.2
    attack_cd = 40

    def __init__(self, scrn):
        super().__init__(scrn,
                         Archer.init_upgrade_cost,
                         Archer.init_level,
                         Archer.init_atk,
                         Archer.init_atk_range,
                         Archer.attack_cd,
                         AttackBlock.arrow_spd,
                         Character.archer_img_file,
                         AttackBlock.arrow
                         )
        self.atkPoint = Archer.init_atk + (self.level * 1.3)

    def level_up(self):
        # Section to implement level up
        if self.upgrade_cost <= 0:
            self.level = self.level + 1
            self.atk_point = Archer.init_atk + (self.level * 1.3)
            self.upgrade_cost = self.get_upgrade_cost()

    def get_upgrade_cost(self):
        return (4 * (self.level ** 3)) / 5