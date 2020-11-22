"""
#Globlin Tower Defense#
##Arthur: Yi Lin##
##Version: Alpha Game##

###Overview###
This project is a game that mimics the Bloon Tower Defense Game.
The goal of the game is to prevent any goblin from approaching the end of the
course.

### Dependencies ###
Please install pygame through
`pip install pygame`

###How to Start###
Please run Gameworld.py to start the game. Execute `python Gameworld.py` at the
root directory of GoblinDefense to start
the game.

###How to Play###
Player can use mouse to select characters from the side navigator on the right
to build defenses against approaching
   goblin.
Please press an hold down the mouse to the select character and drag it to
desire location.
The transparent black circle is the attack range of the player. Please use it
as a reference when placing the character
Player can release the mouse press to place the character
The character can only be placed in the plane outside of the road.
Place character in the road and in select will be omitted
After placing characters in the desire area, the player can press the start
button in the side navigator to start the
game.
The goblin will spawn at the top right and start to move to the end of the
course.
During the game, the player can click on the character to see the status of the
character which is render in the side
navigator.
In the side navigator, the player can click release to remove the character and
get a portion of the cost to hired the
character.
During the game, the player can press the pause button in the side navigator to
pause game.
Player can press the pause button again to resume the game
During the game, the player can press the quit button in the side navigator to
quit the game.
The windows X (exit) button will not exit the game. It is temporarily a restart
button.

### Issues to Fix ###
Improve the game levels and the logic to spawn goblins
Improve feedback system display for the characters, the player, and the buttons

"""

import pygame
import random
from DataModel.Color import Color
from DataModel.GameCourse.GameCourse import GameCourse
from DataModel.Entity.Characters.AtkRangeBlk import AtkRangeBlk
from DataModel.Entity.Goblins.Goblin import Goblin
from DataModel.Entity.Goblins.Hobgoblin import Hobgoblin
from DataModel.Entity.Goblins.GoblinShaman import GoblinShaman
from DataModel.Entity.Goblins.GoblinLord import GoblinLord
from DataModel.FeedbackSystem.FeedbackSystem import FeedbackSystem
from DataModel.Player.Player import Player

pygame.init()
pygame.font.init()
pygame.mixer.init()


# Initialize Pygame
class Gameworld:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    START_POS = ((GameCourse.roadsDef[0][0] +
                  (GameCourse.roadsDef[0][2] // 2)),
                 GameCourse.roadsDef[0][1])
    FONT = pygame.font.SysFont("serif", 15)
    BGM_FILE = "Ext/sound/GoblinSlayerBgm.mp3"
    SPLASH_IMG = "Ext/imageForSplashScreen.png"
    BG_IMG = "Ext/tiled/gassland.png"

    def __init__(self):
        self.screen = pygame.display.set_mode([Gameworld.SCREEN_WIDTH,
                                               Gameworld.SCREEN_HEIGHT])
        self.course = GameCourse(self.screen)
        self.player = Player("YI LIN")
        self.feedback_system_group = pygame.sprite.Group()
        self.feedback_system = FeedbackSystem(self.screen, self.player)
        self.feedback_system_group.add(self.feedback_system)
        self.done = False
        self.bg = pygame.image.load(Gameworld.BG_IMG)
        self.bg = pygame.transform.scale(self.bg,
                                         (Gameworld.SCREEN_WIDTH,
                                          Gameworld.SCREEN_HEIGHT))
        self.fps = pygame.time.Clock()
        self.chara_group = pygame.sprite.Group()
        self.atk_range_group = pygame.sprite.Group()
        self.select_atk_rge = pygame.sprite.Group()
        self.atk_group = pygame.sprite.Group()
        self.poten_new_char = None
        self.character_class = None
        self.poten_atk_range = None
        self.goblin_group = pygame.sprite.Group()
        self.goblin_cd = 0
        self.goblinshaman_cd = 8
        self.hobgoblin_cd = 10
        self.goblinlord_cd = 15
        self.splash_txt = Gameworld.FONT.render("Press any Key to start the " +
                                                " game. Press Escape to end " +
                                                "the game.", True, Color.BLACK)
        self.game_over_text = Gameworld.FONT.render(
            "The game is over. Right click to restart the game and Left" +
            " click to end the game", True, Color.BLACK)
        self.game_over = False
        self.is_splashing = True

        self.start = False
        self.pause = False
        self.mute = False

    def restart(self):
        self.stop_bgm()
        self.__init__()

    def draw_splash(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.done = True
                else:
                    self.is_splashing = False
        self.screen.fill(Color.WHITE)
        splash_img = pygame.image.load(Gameworld.SPLASH_IMG).convert_alpha()
        self.screen.blit(splash_img, (0, 0))
        rect = self.screen.get_rect()
        text_box_x = (self.SCREEN_WIDTH - self.splash_txt.get_width()) // 2
        text_box_y = (self.SCREEN_HEIGHT - self.splash_txt.get_height()) // 2
        pygame.draw.rect(self.screen, Color.GREEN,
                         [rect.x + text_box_x, text_box_y,
                          self.splash_txt.get_width(),
                          self.splash_txt.get_height()
                          ])
        self.screen.blit(self.splash_txt, [text_box_x, text_box_y])
        pygame.display.flip()
        self.fps.tick(20)

    def run(self):
        self.restart()
        while not self.done:
            if self.is_splashing:
                self.draw_splash()
            else:
                self.game_logic()
                self.handle_user_input()

                self.draw()
                # Go ahead and update the screen with what we've drawn.

            pygame.display.flip()

            # Limit to 20 frames per second
            self.fps.tick(20)

    def game_logic(self):
        # check if player is able to continue to play and if the game is pause
        if self.player.health > 0 and not self.pause:
            if self.start:
                self.start = self.player.update()
                # Spawn new goblin
                if self.goblin_cd <= 0:
                    if self.player.game_lvl < 16:
                        start_range = 16 - self.player.game_lvl
                        end_range = 18 - self.player.game_lvl
                    else:
                        start_range = 1
                        end_range = 2
                    self.goblin_cd = random.randrange(start_range, end_range)
                    self.player.num_to_defeat = self.player.num_to_defeat + 1
                    self.add_goblin("")
                if self.goblinshaman_cd <= 0:
                    if self.player.game_lvl < 32:
                        start_range = 32 - self.player.game_lvl
                        end_range = 35 - self.player.game_lvl
                    else:
                        start_range = 1
                        end_range = 3
                    self.goblinshaman_cd = random.randrange(start_range, end_range)
                    self.player.num_to_defeat = self.player.num_to_defeat + 1
                    self.add_goblin("shaman")
                if self.hobgoblin_cd <= 0:
                    if self.player.game_lvl < 48:
                        start_range = 48 - self.player.game_lvl
                        end_range = 52 - self.player.game_lvl
                    else:
                        start_range = 1
                        end_range = 4
                    self.hobgoblin_cd = random.randrange(start_range, end_range)
                    self.player.num_to_defeat = self.player.num_to_defeat + 1
                    self.add_goblin("hob")
                if self.goblinlord_cd <= 0:
                    if self.player.game_lvl < 64:
                        start_range = 64 - self.player.game_lvl
                        end_range = 69 - self.player.game_lvl
                    else:
                        start_range = 1
                        end_range = 5
                    self.goblinlord_cd = random.randrange(start_range, end_range)
                    self.player.num_to_defeat = self.player.num_to_defeat + 1
                    self.add_goblin("lord")

                self.goblin_cd = self.goblin_cd - 1
                self.goblinlord_cd = self.goblinlord_cd - 1
                self.hobgoblin_cd = self.hobgoblin_cd - 1
                self.goblinshaman_cd = self.goblinshaman_cd - 1

            # Handle the goblin when it reach to the end of the course
            for goblin in self.goblin_group:
                if len(goblin.point_to_move) == 0:
                    self.player.health = self.player.health - 1
                    self.goblin_group.remove(goblin)

            # Hightlight start button gray (allow new click) if there is
            #    existing goblin
            if not self.goblin_group:
                start_btn = self.feedback_system.btn_array[0]
                start_btn.image.fill(Color.GRAY)
                start_btn.image.blit(start_btn.render_text, [0, 0])
            else:
                start_btn = self.feedback_system.btn_array[0]
                start_btn.image.fill(Color.RED)
                start_btn.image.blit(start_btn.render_text, [0, 0])

            # Collision Dectection on hired characters' attack range and goblin
            #     to initiate attack
            for atk_range in self.atk_range_group:
                for goblin in self.goblin_group:
                    if pygame.sprite.collide_circle(atk_range, goblin):
                        atk_blk = atk_range.src_chara.attack(goblin)
                        if atk_blk is not None:
                            if self.mute is not True:
                                atk_blk.shot_sound()
                            self.atk_group.add(atk_blk)

            # Handle attack block being initiated
            for atk_blk in self.atk_group:
                if atk_blk.landed:
                    self.atk_group.remove(atk_blk)
                else:
                    gg = self.goblin_group
                    hitted_goblins = pygame.sprite.spritecollide(atk_blk,
                                                                 gg,
                                                                 False)
                    if len(hitted_goblins) > 0:
                        self.atk_group.remove(atk_blk)
                        hit_goblin = hitted_goblins[0]
                        hit_goblin.health = hit_goblin.health - atk_blk.damage
                        if hit_goblin.health <= 0:
                            self.player.budget += hit_goblin.reward
                            self.goblin_group.remove(hit_goblin)
                            atk_blk.source.upgrade_cost -= 1
                        else:
                            if atk_blk.effect == "slow":
                                if hit_goblin.speed > 3:
                                    hit_goblin.speed = hit_goblin.speed - 1
                                else:
                                    hit_goblin.speed = 3
            self.atk_group.update()
            self.goblin_group.update()
        elif self.player.health <= 0:
            self.game_over = True
            self.stop_bgm()

        # Handle mute logic
        if self.mute:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        self.chara_group.update()
        self.feedback_system_group.update()

    def handle_user_input(self):
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            # Check if the player press the window (x) button
            if event.type == pygame.QUIT:
                self.done = True

            # Check if the player lose the game
            elif self.game_over:
                mouse_press = pygame.mouse.get_pressed()
                # Check for left click to end the game
                if mouse_press[0]:
                    self.done = True
                    self.game_over = True
                # Check for right click to restart the game
                elif mouse_press[2]:
                    self.done = True
                    self.game_over = False

            # check if the player clicked on element in the feedback system on
            #   the right
            elif mouse_pos[0] > FeedbackSystem.framework_pos[0]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.character_class = None
                    # Check if any button is clicked
                    button_click = self.feedback_system.click_button(mouse_pos)
                    # Handle Button Click
                    if button_click[0] == 0 and button_click[1] is True:
                        # Handle start button click
                        if not self.start and not self.goblin_group:
                            self.start = True
                            self.play_bgm()
                            self.add_goblin("")
                    elif button_click[0] == 1 and button_click[1] is True:
                        # Handle pause button click
                        self.pause = False if self.pause else True
                    elif button_click[0] == 2 and button_click[1] is True:
                        # Handle quit button click
                        self.done = True
                        self.game_over = True
                    elif button_click[0] == 3 and button_click[1] is True:
                        # Handle mute button click
                        self.mute = False if self.mute else True

                    # Check if a selected character is to be release
                    rel_click = self.feedback_system.click_release(mouse_pos)
                    if rel_click:
                        self.select_atk_rge.empty()
                        atk = self.feedback_system.clicked_chara.atk_range_blk
                        self.atk_range_group.remove(atk)
                        clicked_chara = self.feedback_system.clicked_chara
                        self.chara_group.remove(clicked_chara)
                        cost = clicked_chara.get_upgrade_cost()
                        incr_amt = cost / 2
                        self.player.budget = self.player.budget + incr_amt
                        self.feedback_system.clicked_chara = None

                    # Check if a new character is being hired
                    self.character_class = self.feedback_system.click_icon(
                        mouse_pos)
                    if self.character_class is not None and \
                            self.player.budget >= \
                            self.character_class.init_upgrade_cost:
                        self.poten_new_char = self.character_class(self.screen)
                        mouse_pos = pygame.mouse.get_pos()
                        self.poten_atk_range = AtkRangeBlk(self.screen,
                                                           Color.BLACK_TRANS,
                                                           mouse_pos,
                                                           self.poten_new_char)
                        self.chara_group.add(self.poten_atk_range)
                        self.chara_group.add(self.poten_new_char)

                # Omitted new character being place in the feedback system
                #   range
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.chara_group.remove(self.poten_atk_range)
                    self.chara_group.remove(self.poten_new_char)
                    self.poten_new_char = None

            # check if the player clicked on element left of the feedback
            #   system
            elif mouse_pos[0] < FeedbackSystem.framework_pos[0]:
                # Place new character being hire from the feedback system
                if self.poten_new_char is not None:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.chara_group.remove(self.poten_new_char)
                        self.chara_group.remove(self.poten_atk_range)
                        char_coli = False
                        for chara in self.chara_group:
                            new_chara = self.poten_new_char
                            char_coli = pygame.sprite.collide_circle(new_chara,
                                                                     chara)
                            if (char_coli):
                                break
                        if not self.course.occupy(self.poten_new_char) \
                                and not char_coli:
                            self.chara_group.remove(self.poten_atk_range)
                            atk_range = self.poten_atk_range
                            self.poten_new_char.atk_range_blk = atk_range
                            self.poten_new_char.draggable = False
                            self.chara_group.add(self.poten_new_char)
                            self.atk_range_group.add(self.poten_atk_range)
                            cost = self.poten_new_char.upgrade_cost
                            self.player.budget = self.player.budget - cost
                            self.poten_new_char = None

                # Render the attack range of hired character being select
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.feedback_system.clicked_chara = None
                    self.character_class = None
                    for chara in self.chara_group:
                        clicked_chara = chara.clicked(mouse_pos)
                        if clicked_chara is not None:
                            atk_range = clicked_chara.atk_range_blk
                            self.atk_range_group.add(atk_range)
                            self.feedback_system.clicked_chara = clicked_chara

    def draw(self):
        # Check if player is still able to play
        if self.player.health > 0:
            # Clear the screen
            self.screen.blit(self.bg, (0, 0))
            self.course.render()
            if self.feedback_system.clicked_chara:
                self.select_atk_rge.empty()
                atk_range = self.feedback_system.clicked_chara.atk_range_blk
                self.select_atk_rge.add(atk_range)
                self.select_atk_rge.draw(self.screen)
            self.chara_group.draw(self.screen)
            self.atk_group.draw(self.screen)
            self.goblin_group.draw(self.screen)
            self.feedback_system_group.draw(self.screen)
            self.feedback_system.draw_player_info()
            self.feedback_system.draw_buttons()
            self.feedback_system.draw_icons()
            if self.character_class is not None:
                chara_cl = self.character_class
                self.feedback_system.show_avail_chara_info(chara_cl)
            self.feedback_system.show_chara_info()
        else:
            # Check the restart frame
            self.screen.set_alpha(127)
            self.screen.fill(Color.WHITE)
            rect = self.screen.get_rect()
            text_box_x = (Gameworld.SCREEN_WIDTH -
                          self.game_over_text.get_width()) // 2
            text_box_y = (Gameworld.SCREEN_HEIGHT -
                          self.game_over_text.get_height()) // 2
            pygame.draw.rect(self.screen, Color.GREEN,
                             [rect.x + text_box_x, text_box_y,
                              self.game_over_text.get_width(),
                              self.game_over_text.get_height()
                              ])
            self.screen.blit(self.game_over_text, [text_box_x, text_box_y])

    def add_goblin(self, goblin_type):
        if goblin_type == "hob":
            self.goblin_group.add(Hobgoblin(Gameworld.START_POS,
                                            Hobgoblin.img_file, self.player.game_lvl))
        elif goblin_type == "shaman":
            self.goblin_group.add(GoblinShaman(Gameworld.START_POS,
                                               GoblinShaman.img_file, self.player.game_lvl))
        elif goblin_type == "lord":
            self.goblin_group.add(GoblinLord(Gameworld.START_POS,
                                             GoblinLord.img_file, self.player.game_lvl))
        else:
            self.goblin_group.add(Goblin(Gameworld.START_POS,
                                         Goblin.img_file, self.player.game_lvl))

    def play_bgm(self):
        pygame.mixer.music.load(Gameworld.BGM_FILE)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

    def stop_bgm(self):
        pygame.mixer.music.stop()


if __name__ == "__main__":
    world = Gameworld()
    while not world.game_over:
        world.run()

pygame.quit()
