"""
Use sprites to collect blocks.

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Explanation video: http://youtu.be/4W2AqUetBi4
"""
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    WIDTH = 20
    HEIGHT = 15

    def __init__(self, color):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface((Block.WIDTH, Block.HEIGHT))
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT)


class BlueBlock(Block):
    # Constructor -- takes a block to copy
    def __init__(self, block):
        super().__init__(BLUE)
        # Copy block parameters to this subclass of Block.
        self.rect.x = block.rect.x
        self.rect.y = block.rect.y

class Player(Block):
    START_X = 10
    START_Y = 10
    def __init__(self):
        super().__init__(RED)

        self.rect.x = Player.START_X
        self.rect.y = Player.START_Y

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

BG = pygame.image.load("C:\\Users\\Admin\\Desktop\\CompSci\\CMPT414N_MSCS_526\\gdp1\\GoblinTowerDefense\\icons\\GoblinSlayer.png")

for i in range(50):
    # This represents a block
    block = Block(BLACK)

    # Set a random location for the block
    block.rect.x = random.randrange(SCREEN_WIDTH - Block.WIDTH)
    block.rect.y = random.randrange(SCREEN_HEIGHT - Block.HEIGHT)

    # Add the block to the list of objects

    # collision detection list
    block_list.add(block)
    # render lists
    all_sprites_list.add(block)

# Create a RED player block
player = Block(RED)
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

            # Clear the screen
    screen.fill(WHITE)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()

    # Fetch the x and y out of the list,
    # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    player.rect.x = pos[0]
    player.rect.y = pos[1]

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

    # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        blueBlk = BlueBlock(block)
        all_sprites_list.add(blueBlk)
        print(score)

    all_sprites_list.remove(player)
    all_sprites_list.add(player)
    # Draw all the spites
    all_sprites_list.draw(screen)


    screen.blit(BG, (100, 200))
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
