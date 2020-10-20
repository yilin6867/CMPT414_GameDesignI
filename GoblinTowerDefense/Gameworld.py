import pygame
from DataModel.GameCourse.GameCourse import GameCourse
from DataModel.Entity.Characters.AtkRangeBlk import atk_range_blk
from DataModel.Entity.Goblins.Goblin import goblin
from DataModel.FeedbackSystem.FeedbackSystem import feedback_system
from DataModel.Player.Player import Player

# Initialize Pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("serif", 15)


class Gameworld():
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    WHITE = (255, 255, 255)
    GREEN = (90, 230, 10)
    BLACK = (0, 0, 0)
    BLACK_TRANS = (0, 0, 0, 127)
    start_pos = ((GameCourse.roadsDef[0][0] + (GameCourse.roadsDef[0][2] // 2)), GameCourse.roadsDef[0][1])

    def __init__(self):
        self.screen = pygame.display.set_mode([Gameworld.SCREEN_WIDTH, Gameworld.SCREEN_HEIGHT])
        self.course = GameCourse(self.screen)
        self.player = Player("Test")
        self.feedback_system_group = pygame.sprite.Group()
        self.feedback_system = feedback_system(self.screen, self.player)
        self.feedback_system_group.add(self.feedback_system)
        self.done = False
        self.fps = pygame.time.Clock()
        self.chara_group = pygame.sprite.Group()
        self.atk_range_group = pygame.sprite.Group()
        self.atk_group = pygame.sprite.Group()
        self.poten_new_char = None
        self.poten_atk_range = None
        self.goblin_group = pygame.sprite.Group()
        self.goblin_cd = 5
        self.game_over_text = font.render("The game is over. Left click to restart the game", True, Gameworld.BLACK)
        self.game_over = False

    def restart(self):
        self.__init__()

    def run(self):
        self.restart()
        while not self.done:
            self.game_logic()
            self.handle_user_input()

            self.chara_group.update()
            self.atk_group.update()
            self.goblin_group.update()
            self.feedback_system_group.update()
            self.draw_background()
            # Go ahead and update the screen with what we've drawn.

            pygame.display.flip()

            # Limit to 60 frames per second
            self.fps.tick(20)

    def game_logic(self):
        if (self.player.health > 0):
            if (self.goblin_cd == 0):
                self.goblin_cd = 100 * (1 - (self.player.game_lvl)/100)
                self.add_goblin()
            else:
                self.goblin_cd = self.goblin_cd -1
            for goblin in self.goblin_group:
                if len(goblin.point_to_move) == 0:
                    self.player.health = self.player.health - 1
                    self.goblin_group.remove(goblin)

            for atk_range in self.atk_range_group:
                list_to_atk = pygame.sprite.spritecollide(atk_range, self.goblin_group, False)
                for goblin in list_to_atk:
                    atk_blk = atk_range.src_chara.attack(goblin)
                    if (atk_blk is not None):
                        self.atk_group.add(atk_blk)

            for atk_blk in self.atk_group:
                if (atk_blk.landed):
                    self.atk_group.remove(atk_blk)
                else:
                    hitted_goblins = pygame.sprite.spritecollide(atk_blk, self.goblin_group, False)
                    if (len(hitted_goblins) > 0):
                        self.atk_group.remove(atk_blk)
                    for goblin in hitted_goblins:
                        goblin.health = goblin.health - atk_blk.damage
                        if (goblin.health <= 0):
                            self.player.budget = self.player.budget + goblin.reward
                            self.goblin_group.remove(goblin)


        else:
            self.game_over = True

    def handle_user_input(self):
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.done = True
            elif self.game_over:
                if (event.type == pygame.MOUSEBUTTONUP):
                    self.done = True
                    self.game_over = False
                    print(self.game_over)
            elif (mouse_pos[0] > feedback_system.framework_pos[0]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    character_class = self.feedback_system.click_icon(mouse_pos)
                    if (character_class is not None):
                        self.poten_new_char = character_class(self.screen)
                        self.poten_atk_range = atk_range_blk(self.screen, Gameworld.BLACK_TRANS,
                                                             pygame.mouse.get_pos(), self.poten_new_char)
                        self.chara_group.add(self.poten_atk_range)
                        self.chara_group.add(self.poten_new_char)
            elif (mouse_pos[0] < feedback_system.framework_pos[0]):
                if self.poten_new_char is not None:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.chara_group.remove(self.poten_new_char)
                        self.chara_group.remove(self.poten_atk_range)
                        self.atk_range_group.add(self.poten_atk_range)
                        self.poten_new_char.dragable = False
                        print(self.poten_new_char.dragable)
                        self.chara_group.add(self.poten_new_char)


    def draw_background(self):
        # Clear the screen
        if (self.player.health < 5):
            self.screen.fill(Gameworld.GREEN)
            self.course.render()
            self.chara_group.draw(self.screen)
            self.atk_range_group.draw(self.screen)
            self.atk_group.draw(self.screen)
            self.goblin_group.draw(self.screen)
            self.feedback_system_group.draw(self.screen)
            self.feedback_system.draw_text()
            self.feedback_system.draw_icons()
        else:
            self.screen.set_alpha(127)
            self.screen.fill(Gameworld.WHITE)
            rect = self.screen.get_rect()
            text_box_x = (Gameworld.SCREEN_WIDTH - self.game_over_text.get_width()) // 2
            text_box_y = (Gameworld.SCREEN_HEIGHT - self.game_over_text.get_height()) // 2
            pygame.draw.rect(self.screen, Gameworld.GREEN, [rect.x + text_box_x, text_box_y
                , self.game_over_text.get_width(), self.game_over_text.get_height()
                                                            ])
            self.screen.blit(self.game_over_text, [text_box_x, text_box_y])


    def add_goblin(self):
        print("add new goblin")
        self.goblin_group.add(goblin(Gameworld.start_pos))

if __name__ == "__main__":
    world = Gameworld()
    while not world.game_over:
        world.run()
        print(world.game_over)

pygame.quit()
