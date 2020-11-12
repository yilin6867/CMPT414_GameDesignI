import math
import pygame
from DataModel.Entity.Entity import Entity


class AttackBlock(Entity):
    dagger = "Ext/attacks/dagger.png"
    dagger_sd = "Ext/sound/Knife-Sharpen-C-www.fesliyanstudios.com.wav"
    arrow = "Ext/attacks/arrow.png"
    arrow_sd = "Ext/sound/BOWMEN1.wav"
    holy_light = "Ext/attacks/holy_light.png"
    holy_light_sd = "Ext/sound/Notification-Bell-C1-www.fesliyanstudios.com.wav"
    fireball = "Ext/attacks/fireball.png"
    fireball_sd = "Ext/sound/Fireball+1.wav"
    dagger_spd = 10
    fireball_spd = 10
    arrow_spd = 15
    holylight_spd = 8
    size = (20, 20)

    def __init__(self, scrn, pos, size, img_file, damage, spd, traceable, target, source, effect):
        super().__init__(pos, size, img_file)
        self.screen = scrn
        self.damage = damage
        self.speed = spd
        self.target = target
        self.landed = False
        self.traceable = traceable
        self.target_x = target.rect.x
        self.target_y = target.rect.y
        self.source = source
        self.effect = effect
        self.img_file = img_file
        self.sound = pygame.mixer.init()

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

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def shot_sound(self):
        if self.img_file == AttackBlock.dagger:
            sound = pygame.mixer.Sound(AttackBlock.dagger_sd)
            pygame.mixer.Channel(0).set_volume(0.05)
            pygame.mixer.Channel(0).play(sound)
        elif self.img_file == AttackBlock.arrow:
            sound = pygame.mixer.Sound(AttackBlock.arrow_sd)
            pygame.mixer.Channel(1).set_volume(0.05)
            pygame.mixer.Channel(1).play(sound)
        elif self.img_file == AttackBlock.fireball:
            sound = pygame.mixer.Sound(AttackBlock.fireball_sd)
            pygame.mixer.Channel(2).set_volume(0.05)
            pygame.mixer.Channel(2).play(sound)
        elif self.img_file == AttackBlock.holy_light:
            sound = pygame.mixer.Sound(AttackBlock.holy_light_sd)
            pygame.mixer.Channel(3).set_volume(0.05)
            pygame.mixer.Channel(3).play(sound)

