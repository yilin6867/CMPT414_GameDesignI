"""
#Globlin Tower Defense#
##Arthur: Yi Lin##
##Version: Alpha Game##

###Overview###
This project is a game that mimics the Bloon Tower Defense Game.
The goal of the game is to prevent any goblin from approaching the end of the course.

### Dependencies ###
Please install pygame through
`pip install pygame`

###Howe to Play###
Player can use mouse to select characters from the side navigator on the right to build defenses against approaching
   goblin.
Please press an hold down the mouse to the select character and drag it to desire location.
The transparent black circle is the attack range of the player. Please use it as a reference when placing the character
Player can release the mouse press to place the character
The character can only be placed in the plane outside of the road.
Place character in the road and in select will be omitted
After placing characters in the desire area, the player can press the start button in the side navigator to start the
game.
The goblin will spawn at the top right and start to move to the end of the course.
During the game, the player can click on the character to see the status of the character which is render in the side
navigator.
In the side navigator, the player can click release to remove the character and get a portion of the cost to hired the
character.
During the game, the player can press the pause button in the side navigator to pause game.
Player can press the pause button again to resume the game
During the game, the player can press the quit button in the side navigator to quit the game.
The windows X (exit) button will not exit the game. It is temporarily a restart button.

### Bugs to fix ###
Prevent the character being place overlapping into the road
Fix the logic of how the Goblin move so it would not seem as it move slightly towards left in the road

### Features plan to Add or Complete ###
Add more characters and goblins into the game
Allow the character to self upgrade based on the number of goblin it defeat.

"""

import pygame
import random
from DataModel.Color import Color
from DataModel.GameCourse.GameCourse import GameCourse
from DataModel.Entity.Characters.AtkRangeBlk import AtkRangeBlk
from DataModel.Entity.Goblins.Goblin import Goblin
from DataModel.FeedbackSystem.FeedbackSystem import FeedbackSystem
from DataModel.Player.Player import Player

# Initialize Pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("serif", 15)
pygame.display.set_caption("Golbin Tower Defense")


class Gameworld:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    start_pos = ((GameCourse.roadsDef[0][0] + (GameCourse.roadsDef[0][2] // 2)), GameCourse.roadsDef[0][1])

    def __init__(self):
        self.screen = pygame.display.set_mode([Gameworld.SCREEN_WIDTH, Gameworld.SCREEN_HEIGHT])
        self.course = GameCourse(self.screen)
        self.player = Player("Test")
        self.feedback_system_group = pygame.sprite.Group()
        self.feedback_system = FeedbackSystem(self.screen, self.player)
        self.feedback_system_group.add(self.feedback_system)
        self.done = False
        self.fps = pygame.time.Clock()
        self.chara_group = pygame.sprite.Group()
        self.atk_range_group = pygame.sprite.Group()
        self.select_atk_rge = pygame.sprite.Group()
        self.atk_group = pygame.sprite.Group()
        self.poten_new_char = None
        self.poten_atk_range = None
        self.goblin_group = pygame.sprite.Group()
        self.goblin_cd = 5
        self.game_over_text = font.render("The game is over. Right click to restart the game and Left click " +
                                          "to end the game", True, Color.BLACK)
        self.game_over = False

        self.start = False
        self.pause = False

    def restart(self):
        self.__init__()

    def run(self):
        self.restart()
        while not self.done:
            self.game_logic()
            self.handle_user_input()

            self.draw()
            # Go ahead and update the screen with what we've drawn.

            pygame.display.flip()

            # Limit to 60 frames per second
            self.fps.tick(60)

    def game_logic(self):
        if self.player.health > 0 and not self.pause:
            if self.start:
                if self.goblin_cd <= 0:
                    end_range = 100 - self.player.game_lvl if self.player.game_lvl < 99 else 2
                    self.goblin_cd = random.randrange(1, end_range)
                    self.add_goblin()
                else:
                    self.goblin_cd = self.goblin_cd - 1

            for goblin in self.goblin_group:
                if len(goblin.point_to_move) == 0:
                    self.player.health = self.player.health - 1
                    self.goblin_group.remove(goblin)

            for atk_range in self.atk_range_group:
                for goblin in self.goblin_group:
                    if pygame.sprite.collide_circle(atk_range, goblin):
                        atk_blk = atk_range.src_chara.attack(goblin)
                        if atk_blk is not None:
                            self.atk_group.add(atk_blk)

            for atk_blk in self.atk_group:
                if atk_blk.landed:
                    self.atk_group.remove(atk_blk)
                else:
                    hitted_goblins = pygame.sprite.spritecollide(atk_blk, self.goblin_group, False)
                    if len(hitted_goblins) > 0:
                        self.atk_group.remove(atk_blk)
                    for hit_goblin in hitted_goblins:
                        hit_goblin.health = hit_goblin.health - atk_blk.damage
                        if hit_goblin.health <= 0:
                            self.player.budget = self.player.budget + hit_goblin.reward
                            self.player.defeat_num = self.player.defeat_num + 1
                            self.goblin_group.remove(hit_goblin)

            self.player.update()
            self.chara_group.update()
            self.atk_group.update()
            self.goblin_group.update()
            self.feedback_system_group.update()
        elif self.player.health <= 0:
            self.game_over = True

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

            # check if the player clicked on element in the feedback system on the right
            elif mouse_pos[0] > FeedbackSystem.framework_pos[0]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any button is clicked
                    button_click = self.feedback_system.click_button(mouse_pos)
                    if button_click[0] == 0 and button_click[1] is True:
                        self.start = True
                    elif button_click[0] == 1 and button_click[1] is True:
                        self.pause = False if self.pause else True
                    elif button_click[0] == 2 and button_click[1] is True:
                        self.done = True
                        self.game_over = True

                    # Check if a selected character is to be release
                    release_click = self.feedback_system.click_release(mouse_pos)
                    if release_click:
                        self.select_atk_rge.empty()
                        self.atk_range_group.remove(self.feedback_system.clicked_chara.atk_range_blk)
                        self.chara_group.remove(self.feedback_system.clicked_chara)
                        incr_amt = self.feedback_system.clicked_chara.init_upgrade_cost // 2
                        self.player.budget = self.player.budget + incr_amt
                        self.feedback_system.clicked_chara = None

                    # Check if a new character is being hired
                    character_class = self.feedback_system.click_icon(mouse_pos)
                    if character_class is not None:
                        self.poten_new_char = character_class(self.screen)
                        self.poten_atk_range = AtkRangeBlk(self.screen, Color.BLACK_TRANS,
                                                           pygame.mouse.get_pos(), self.poten_new_char)
                        self.chara_group.add(self.poten_atk_range)
                        self.chara_group.add(self.poten_new_char)

                # Omitted new character being place in the feedback system range
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.chara_group.remove(self.poten_atk_range)
                    self.chara_group.remove(self.poten_new_char)
                    self.poten_new_char = None

            # check if the player clicked on element left of the feedback system
            elif mouse_pos[0] < FeedbackSystem.framework_pos[0]:
                # Place new character being hire from the feedback system
                if self.poten_new_char is not None:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.chara_group.remove(self.poten_new_char)
                        self.chara_group.remove(self.poten_atk_range)
                        if not self.course.occupy(mouse_pos) \
                                and not pygame.sprite.spritecollide(self.poten_new_char, self.chara_group, False):
                            self.chara_group.remove(self.poten_atk_range)
                            self.poten_new_char.atk_range_blk = self.poten_atk_range
                            self.poten_new_char.draggable = False
                            self.chara_group.add(self.poten_new_char)
                            self.atk_range_group.add(self.poten_atk_range)
                            self.player.budget = self.player.budget - self.poten_new_char.upgrade_cost
                            self.poten_new_char = None

                # Render the attack range of hired character being select
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.feedback_system.clicked_chara = None
                    clicked_chara = None
                    for chara in self.chara_group:
                        clicked_chara = chara.clicked(mouse_pos)
                        if clicked_chara is not None:
                            self.atk_range_group.add(clicked_chara.atk_range_blk)
                            self.feedback_system.clicked_chara = clicked_chara

    def draw(self):
        # Check if player is still able to play
        if self.player.health > 0:
            # Clear the screen
            self.screen.fill(Color.GREEN)
            self.course.render()
            if self.feedback_system.clicked_chara:
                self.select_atk_rge.empty()
                self.select_atk_rge.add(self.feedback_system.clicked_chara.atk_range_blk)
                self.select_atk_rge.draw(self.screen)
            self.chara_group.draw(self.screen)
            self.atk_group.draw(self.screen)
            self.goblin_group.draw(self.screen)
            self.feedback_system_group.draw(self.screen)
            self.feedback_system.draw_player_info()
            self.feedback_system.draw_buttons()
            self.feedback_system.draw_icons()
            self.feedback_system.show_chara_info()
        else:
            # Check the restart frame
            self.screen.set_alpha(127)
            self.screen.fill(Color.WHITE)
            rect = self.screen.get_rect()
            text_box_x = (Gameworld.SCREEN_WIDTH - self.game_over_text.get_width()) // 2
            text_box_y = (Gameworld.SCREEN_HEIGHT - self.game_over_text.get_height()) // 2
            pygame.draw.rect(self.screen, Color.GREEN,
                             [rect.x + text_box_x, text_box_y, self.game_over_text.get_width(),
                              self.game_over_text.get_height()
                              ])
            self.screen.blit(self.game_over_text, [text_box_x, text_box_y])

    def add_goblin(self):
        self.goblin_group.add(Goblin(Gameworld.start_pos))


if __name__ == "__main__":
    world = Gameworld()
    while not world.game_over:
        world.run()

pygame.quit()
