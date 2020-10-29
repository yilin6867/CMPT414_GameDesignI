import math
from DataModel.Entity.Entity import Entity


class AttackBlock(Entity):
    rock = "icons/attacks/rock.jpg"
    rock_spd = 5
    size = (10, 10)

    def __init__(self, scrn, pos, size, img_file, damage, traceable, target):
        super().__init__(pos, size, img_file)
        self.screen = scrn
        self.damage = damage
        self.speed = AttackBlock.rock_spd
        self.target = target
        self.landed = False
        self.traceable = traceable
        self.target_x = target.rect.x
        self.target_y = target.rect.y

    def update(self):
        # Determine if attack can follow the enemy
        if self.traceable:
            target_x = self.target.rect.x
            target_y = self.target.rect.y
        else:
            target_x = self.target_x
            target_y = self.target_y

        # Move the attack block to change the target coordinates
        diff_x = target_x - self.rect.x
        diff_y = target_y - self.rect.y

        angle = math.atan2(diff_x, diff_y)
        next_x = self.speed * math.sin(angle)
        next_y = self.speed * math.cos(angle)

        if (self.rect.x >= target_x - self.speed +1 and self.rect.x <= target_x + self.speed-1) and (
                self.rect.y >= target_y - self.speed +1 and self.rect.y <= target_y + self.speed-1):
            self.rect.x = target_x
            self.rect.y = target_y
            self.landed = True
        else:
            self.rect.x = self.rect.x + math.floor(next_x)
            self.rect.y = self.rect.y + math.floor(next_y)
