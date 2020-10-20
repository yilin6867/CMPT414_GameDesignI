import pygame
#from data_model.Player.player import player
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.GoblinSlayer import GoblinSlayer
from DataModel.FeedbackSystem.Icon import icon

BLACK=(0, 0, 0)

class feedback_system(pygame.sprite.Sprite):
    framework_size = [120, 480]
    framework_pos = [570, 10]
    icon_size = 60
    icon_characters = [GoblinSlayer]

    def __init__(self, scrn, player):
        super().__init__()
        self.screen = scrn
        self.image = pygame.Surface(feedback_system.framework_size)
        self.image.set_alpha(128)
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = feedback_system.framework_pos[0]
        self.rect.y = feedback_system.framework_pos[1]
        self.rect.width = 1
        self.chara_icons = pygame.sprite.Group()
        self.icon_list = []
        self.player = player
        self.player_name = player.name
        self.budget = player.budget
        self.game_lvl = player.game_lvl
        self.health = player.health
        self.next_y_pos = feedback_system.framework_pos[1]
        self.next_x_pos = feedback_system.framework_pos[0]
        self.draw_text()
        self.init_chara_icons()

    def update(self):
        self.budget = self.player.budget
        self.game_lvl = self.player.game_lvl
        self.health = self.player.health

    def init_chara_icons(self):
        for img_idx, img_file in enumerate(Character.img_files):
            x = self.next_x_pos
            y = self.next_y_pos
            chara_icon = icon(img_file, img_idx, x, y, Character.size)
            #chara_icon = icon("../../" + img_file, x, y, character.size)
            self.next_x_pos = self.next_x_pos + feedback_system.icon_size
            if (self.next_x_pos >= feedback_system.framework_pos[0] + feedback_system.framework_size[0]):
                self.next_x_pos = feedback_system.framework_pos[0]
                self.next_y_pos = self.next_y_pos + feedback_system.icon_size
            self.chara_icons.add(chara_icon)
            self.icon_list.append(chara_icon)

    def draw_icons(self):
        self.chara_icons.draw(self.screen)

    def draw_text(self):
        pygame.font.init()
        self.next_y_pos = feedback_system.framework_pos[1]
        font = pygame.font.SysFont("serif", 15)
        budget_txt = font.render("Budget: " + str(self.budget), True, BLACK)
        name_txt = font.render("Name: " + str(self.player_name), True, BLACK)
        lvl_txt = font.render("Game Level: " + str(self.game_lvl), True, BLACK)
        health_txt = font.render("Health: " + str(self.health), True, BLACK)
        self.screen.blit(name_txt, [feedback_system.framework_pos[0], self.next_y_pos])
        self.next_y_pos = self.next_y_pos + name_txt.get_height()
        self.screen.blit(budget_txt, [feedback_system.framework_pos[0], self.next_y_pos])
        self.next_y_pos = self.next_y_pos + budget_txt.get_height()
        self.screen.blit(lvl_txt, [feedback_system.framework_pos[0], self.next_y_pos])
        self.next_y_pos = self.next_y_pos + lvl_txt.get_height()
        self.screen.blit(health_txt, [feedback_system.framework_pos[0], self.next_y_pos])
        self.next_y_pos = self.next_y_pos + health_txt.get_height()

    def click_icon(self, mouse_pos):
        character_idx = None
        for chara_icon in self.icon_list:
            character_idx = chara_icon.on_click(mouse_pos)

        if character_idx is not None:
            print(character_idx, feedback_system.icon_characters[character_idx])
            return feedback_system.icon_characters[character_idx]
        else:
            return None

# pygame.init()
# clock = pygame.time.Clock()
# done = False
# screen = pygame.display.set_mode([700, 500])
# testPlayer = player("Testing")
# testGroup = pygame.sprite.Group()
# test = feedback_system(screen, testPlayer)
# testGroup.add(test)
# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#
#     screen.fill((255, 255, 255))
#     testGroup.draw(screen)
#     test.draw_text()
#     test.draw_icons()
#     pygame.display.flip()
#     clock.tick(60)