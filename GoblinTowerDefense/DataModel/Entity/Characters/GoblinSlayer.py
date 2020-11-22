import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class GoblinSlayer(Character):
    init_level = 1
    init_upgrade_cost = init_level ** 3
    init_atk = 5
    init_atk_range = 100
    attack_growth = 1.3
    attack_cd = 30

    def __init__(self, scrn):
        super().__init__(scrn,
                         GoblinSlayer.init_upgrade_cost,
                         GoblinSlayer.init_level,
                         GoblinSlayer.init_atk,
                         GoblinSlayer.init_atk_range,
                         GoblinSlayer.attack_cd,
                         AttackBlock.dagger_spd,
                         Character.goblinslayer_img_file,
                         AttackBlock.dagger
                         )
        self.atkPoint = GoblinSlayer.init_atk + (self.level * 1.3)

    def level_up(self):
        # Section to implement level up
        if self.upgrade_cost <= 0:
            self.level = self.level + 1
            self.atk_point = GoblinSlayer.init_atk + (self.level * 1.3)
            self.upgrade_cost = self.get_upgrade_cost()

    def get_upgrade_cost(self):
        return self.level ** 3
