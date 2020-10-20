import pygame
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.AttackBlock.AttackBlock import AttackBlock


class GoblinSlayer(Character):
    initUpgradeCost = 5
    initlevel = 0
    initAtk = 5
    initAtkRange = 100
    attackGrowth = 1.3
    attck_cd = 6

    def __init__(self, scrn):
        super().__init__(scrn,
                         GoblinSlayer.initUpgradeCost,
                         GoblinSlayer.initlevel,
                         GoblinSlayer.initAtk,
                         GoblinSlayer.initAtkRange,
                         GoblinSlayer.attck_cd,
                         Character.swordman_img_file,
                         AttackBlock.rock
                         )

    def update(self):
        if self.dragable:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = mouse_pos[0] - self.size[0] // 2
            self.rect.y = mouse_pos[1] - self.size[0] // 2
        if self.upgrade_cost == 0:
            self.level = self.level + 1
            self.atkPoint = GoblinSlayer.initAtk + (self.level * 1.3)

