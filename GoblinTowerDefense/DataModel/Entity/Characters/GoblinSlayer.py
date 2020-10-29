import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class GoblinSlayer(Character):
    init_upgrade_cost = 5
    init_level = 0
    init_atk = 5
    init_atk_range = 100
    attack_growth = 1.3
    attack_cd = 10

    def __init__(self, scrn):
        super().__init__(scrn,
                         GoblinSlayer.init_upgrade_cost,
                         GoblinSlayer.init_level,
                         GoblinSlayer.init_atk,
                         GoblinSlayer.init_atk_range,
                         GoblinSlayer.attack_cd,
                         Character.swordman_img_file,
                         AttackBlock.rock
                         )
        self.atkPoint = GoblinSlayer.init_atk + (self.level * 1.3)

    def update(self):
        # Allow character to be move around before being place on a location
        if self.draggable:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = mouse_pos[0] - self.size[0] // 2
            self.rect.y = mouse_pos[1] - self.size[0] // 2

        # Section to implement level up
        if self.upgrade_cost == 0:
            self.level = self.level + 1
            self.atkPoint = GoblinSlayer.init_atk + (self.level * 1.3)

    def attack(self, enemy):
        if self.atk_cd == 0:
            self.atk_cd = self.def_atk_cd
            attack_coords = [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2]
            return AttackBlock(self.screen, attack_coords, AttackBlock.size, self.atk_img_file, self.atk_point, False,
                               enemy)
        else:
            self.atk_cd = self.atk_cd - 1
            return None
