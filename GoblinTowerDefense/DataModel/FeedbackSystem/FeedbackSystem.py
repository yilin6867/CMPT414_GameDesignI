import pygame
from DataModel.Color import Color
from DataModel.Entity.Characters.Character import Character
from DataModel.Entity.Characters.GoblinSlayer import GoblinSlayer
from DataModel.Entity.Characters.Archer import Archer
from DataModel.Entity.Characters.Priest import Priest
from DataModel.Entity.Characters.Wizard import Wizard
from DataModel.FeedbackSystem.Icon import Icon
from DataModel.FeedbackSystem.Button import Button

pygame.font.init()
font = pygame.font.SysFont("serif", 14)


class FeedbackSystem(pygame.sprite.Sprite):
    framework_size = [120, 480]
    framework_pos = [570, 10]
    icon_size = 60
    icon_characters = [GoblinSlayer, Archer, Priest, Wizard]
    line_space = 5
    section_space = 10

    def __init__(self, scrn, player):
        super().__init__()
        self.screen = scrn
        self.image = pygame.Surface(FeedbackSystem.framework_size)
        self.image.set_alpha(128)
        self.image.fill(Color.GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = FeedbackSystem.framework_pos[0]
        self.rect.y = FeedbackSystem.framework_pos[1]
        self.rect.width = 1
        self.chara_icons = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.btn_array = []
        self.icon_list = []
        self.player = player
        self.player_name = player.name
        self.budget = player.budget
        self.game_lvl = player.game_lvl
        self.health = player.health
        self.next_y_pos = FeedbackSystem.framework_pos[1]
        self.next_x_pos = FeedbackSystem.framework_pos[0]
        self.draw_player_info()
        self.init_buttons()
        self.init_chara_icons()
        self.clicked_chara = None
        self.cancel_btn_info = []

    def update(self):
        # Update player information being display
        self.budget = self.player.budget
        self.game_lvl = self.player.game_lvl
        self.health = self.player.health

    def init_buttons(self):
        self.next_y_pos = self.next_y_pos + 10
        self.next_x_pos = self.next_x_pos + 5

        start_text = font.render("Start", True, Color.BLACK)
        start_btn = Button((self.next_x_pos, self.next_y_pos),
                           (start_text.get_width(), start_text.get_height()), start_text)
        self.next_x_pos = self.next_x_pos + start_text.get_width() + FeedbackSystem.section_space

        pause_text = font.render("Pause", True, Color.BLACK)
        pause_btn = Button((self.next_x_pos, self.next_y_pos),
                           (pause_text.get_width(), pause_text.get_height()), pause_text)
        self.next_x_pos = self.next_x_pos + pause_text.get_width() + FeedbackSystem.section_space

        quit_text = font.render("Quit", True, Color.BLACK)
        quit_btn = Button((self.next_x_pos, self.next_y_pos),
                          (quit_text.get_width(), quit_text.get_height()), quit_text)
        self.next_y_pos = self.next_y_pos + quit_text.get_height() + FeedbackSystem.section_space
        self.next_x_pos = FeedbackSystem.framework_pos[0] + 5
        mute_text = font.render("Mute", True, Color.BLACK)
        mute_btn = Button((self.next_x_pos, self.next_y_pos),
                          (mute_text.get_width(), mute_text.get_height()), mute_text)
        self.next_y_pos = self.next_y_pos + quit_text.get_height() + FeedbackSystem.section_space
        self.buttons.add(start_btn)
        self.buttons.add(pause_btn)
        self.buttons.add(quit_btn)
        self.buttons.add(mute_btn)
        self.btn_array = [start_btn, pause_btn, quit_btn, mute_btn]

    def init_chara_icons(self):
        # Display characters that are listed in array of character image file
        for img_idx, img_file in enumerate(Character.img_files):
            x = self.next_x_pos
            y = self.next_y_pos
            chara_icon = Icon(img_file, img_idx, x, y, Character.size)
            self.next_x_pos = self.next_x_pos + FeedbackSystem.icon_size
            if self.next_x_pos >= FeedbackSystem.framework_pos[0] + FeedbackSystem.framework_size[0]:
                self.next_x_pos = FeedbackSystem.framework_pos[0] + 5
                self.next_y_pos = self.next_y_pos + FeedbackSystem.icon_size
            self.chara_icons.add(chara_icon)
            self.icon_list.append(chara_icon)

    # Check if a character is selected, if so render that character information
    def show_chara_info(self):
        if self.clicked_chara:
            self.chara_info_text(self.clicked_chara)

    def draw_icons(self):
        self.chara_icons.draw(self.screen)


    def draw_player_info(self):
        self.next_y_pos = FeedbackSystem.framework_pos[1]
        x_corrd = FeedbackSystem.framework_pos[0] + 5
        budget_txt = font.render("Budget: " + str(round(self.budget, 2)), True, Color.BLACK)
        name_txt = font.render("Name: " + str(self.player_name), True, Color.BLACK)
        lvl_txt = font.render("Game Level: " + str(self.game_lvl), True, Color.BLACK)
        health_txt = font.render("Health: " + str(self.health), True, Color.BLACK)
        self.screen.blit(name_txt, [x_corrd, self.next_y_pos])
        self.next_y_pos = self.next_y_pos + name_txt.get_height() + FeedbackSystem.line_space
        self.screen.blit(budget_txt, [x_corrd, self.next_y_pos])
        self.next_y_pos = self.next_y_pos + budget_txt.get_height() + FeedbackSystem.line_space
        self.screen.blit(lvl_txt, [x_corrd, self.next_y_pos])
        self.next_y_pos = self.next_y_pos + lvl_txt.get_height() + FeedbackSystem.line_space
        self.screen.blit(health_txt, [x_corrd, self.next_y_pos])
        self.next_y_pos = self.next_y_pos + health_txt.get_height() + FeedbackSystem.line_space

    def draw_buttons(self):
        self.buttons.draw(self.screen)

    def chara_info_text(self, chara):
        # Render the character information if a character is being clicked

        chara_info_pos_y = FeedbackSystem.framework_pos[1] + FeedbackSystem.framework_size[1]
        cancel_text = font.render("Release", True, Color.RED)
        upgrade_cost_text = font.render("Upgrade Cost: " + str(round(chara.upgrade_cost, 2)), True, Color.BLACK)
        atk_range_text = font.render("Attack Range: " + str(chara.atk_range), True, Color.BLACK)
        atk_cd_text = font.render("Attack Rate: 1/" + str(type(chara).attack_cd) + "fps", True, Color.BLACK)
        atk_pt_text = font.render("Attack Point: " + str(chara.atk_point), True, Color.BLACK)
        lvl_text = font.render("Level: " + str(chara.level), True, Color.BLACK)
        name_text = font.render("Name: " + str(type(chara).__name__), True, Color.BLACK)
        chara_info_pos_y = chara_info_pos_y - cancel_text.get_height() - FeedbackSystem.line_space
        self.cancel_btn_info = [FeedbackSystem.framework_pos[0], chara_info_pos_y, cancel_text.get_width(),
                                cancel_text.get_height()]
        self.screen.blit(cancel_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - upgrade_cost_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(upgrade_cost_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_range_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_range_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_cd_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_cd_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_pt_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_pt_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - lvl_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(lvl_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - name_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(name_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])

    def show_avail_chara_info(self, clicked_chara):
        # Render the character information if a character is being clicked
        chara_info_pos_y = FeedbackSystem.framework_pos[1] + FeedbackSystem.framework_size[1]
        upgrade_cost_text = font.render("Hire Cost: " + str(round(clicked_chara.init_upgrade_cost, 2)), True, Color.BLACK)
        atk_range_text = font.render("Attack Range: " + str(clicked_chara.init_atk_range), True, Color.BLACK)
        atk_cd_text = font.render("Attack Rate: 1/" + str(clicked_chara.attack_cd) + "fps", True, Color.BLACK)
        atk_pt_text = font.render("Attack Point: " + str(clicked_chara.init_atk), True, Color.BLACK)
        name_text = font.render("Name: " + str(clicked_chara.__name__), True, Color.BLACK)
        chara_info_pos_y = chara_info_pos_y - upgrade_cost_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(upgrade_cost_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_range_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_range_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_cd_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_cd_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - atk_pt_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(atk_pt_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])
        chara_info_pos_y = chara_info_pos_y - name_text.get_height() - FeedbackSystem.line_space
        self.screen.blit(name_text, [FeedbackSystem.framework_pos[0], chara_info_pos_y])

    # Check if any character in the character display is selected
    def click_icon(self, mouse_pos):
        self.clicked_chara = None
        character_idx = None
        for chara_icon in self.icon_list:
            character_idx = chara_icon.on_click(mouse_pos)
            if character_idx is not None:
                break
        if character_idx is not None:
            clicked_chara = FeedbackSystem.icon_characters[character_idx]
            self.show_avail_chara_info(clicked_chara)
            return clicked_chara
        else:
            return None

    # Check if any button being render is clicked
    def click_button(self, mouse_pos):
        for btn_idx, button in enumerate(self.buttons):
            if button.click(mouse_pos):
                return btn_idx, True, button
        return -1, False, None

    # Check if the release button is being clicked.
    def click_release(self, mouse_pos):
        if self.clicked_chara is not None:
            x_range = self.cancel_btn_info[0] + self.cancel_btn_info[2]
            y_range = self.cancel_btn_info[1] + self.cancel_btn_info[3]
            if (mouse_pos[0] >= self.cancel_btn_info[0] and mouse_pos[0] <= x_range) and (
                    mouse_pos[1] >= self.cancel_btn_info[1] and mouse_pos[1] <= y_range):
                return True
            else:
                return False
        else:
            return False
