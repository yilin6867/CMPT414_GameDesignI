"""
Show the proper way to organize a game using the a game class.

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Explanation video: http://youtu.be/O4Y5KrNgP_c
"""

import pygame
import random

#--- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# --- Classes ---

class Block(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """
    WIDTH = 20
    HEIGHT = 20
    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([Block.WIDTH, Block.HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH-Block.WIDTH)

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += 1

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    WIDTH = 20
    HEIGHT = 20
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([Player.WIDTH, Player.HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Feedback_blk(pygame.sprite.Sprite):
    # Constructor -- takes a block to copy
    HEIGHT = 40
    WIDTH = 100
    def __init__(self):
        super().__init__()
        # Copy block parameters to this subclass of Block.
        self.image = pygame.Surface([Feedback_blk.WIDTH, Feedback_blk.HEIGHT])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - Feedback_blk.WIDTH
        self.rect.y = SCREEN_HEIGHT - Feedback_blk.HEIGHT

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    # --- Class attributes.
    # In this case, all the data we need
    # to run our game.

    # Sprite lists
    block_list = None
    all_sprites_list = None
    player = None

    # Other data
    game_over = False
    score = 0

    # Feedback Block

    # --- Class methods
    # Set up the game
    def __init__(self):
        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(50):
            block = Block()

            block.rect.x = random.randrange(SCREEN_WIDTH - Block.WIDTH)
            block.rect.y = random.randrange(-300, SCREEN_HEIGHT)

            self.block_list.add(block)
            self.all_sprites_list.add(block)

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)

        # Initialize Sound for the game
        self.sound = pygame.mixer.Sound("laser5.ogg")

        # Feedback Initial
        blueBlck = Feedback_blk()
        self.all_sprites_list.add(blueBlck)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()

            # See if the player block has collided with anything.
            blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

            # Check the list of collisions.
            for block in blocks_hit_list:
                self.sound.play()
                self.score += 1
                print(self.score)
                # You can do something with "block" here.

            if len(self.block_list) == 0:
                self.game_over = True

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        self.display_feedback(screen)
        pygame.display.flip()

    def display_feedback(self, screen):
        score_str = "Score: " + str(self.score)
        font = pygame.font.SysFont("serif", 25)
        text = font.render(score_str, True, BLACK)
        center_x = (SCREEN_WIDTH - Feedback_blk.WIDTH // 2) - (text.get_width() // 2)
        center_y = (SCREEN_HEIGHT - Feedback_blk.HEIGHT// 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
