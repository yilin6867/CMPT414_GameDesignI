"""
 Show how to use a sprite backed by a graphic.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""
import random

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Rectangle:
    def __init__(self, color, x, y, width, height, change_x, change_y):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.change_x = change_x
        self.change_y = change_y

    def draw(self, scr, color):
        pygame.draw.rect(scr, self.color, [self.x, self.y, self.width, self.height])

    def move(self):
        self.x = self.x + self.change_x
        self.y = self.y + self.change_y


class Ellipse(Rectangle):
    def draw(self, scr, color):
        pygame.draw.ellipse(scr, self.color, [self.x, self.y, self.width, self.height])


def createObject(object_list, object_class, num_object):
    for _ in range(num_object):
        x = random.randint(x_range[0], x_range[1])
        y = random.randint(y_range[0], y_range[1])
        width = random.randint(width_range[0], width_range[1])
        height = random.randint(height_range[0], height_range[1])
        change_x = random.randint(move_range[0], move_range[1])
        change_y = random.randint(move_range[0], move_range[1])
        color_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        my_object = object_class(color_rgb, x, y, width, height, change_x, change_y)
        object_list.append(my_object)


pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

x_range = (0, 700)
y_range = (0, 500)
width_range = (20, 70)
height_range = (20, 70)
move_range = (-3, 3)

my_list = []
createObject(my_list, Rectangle, 1000)
createObject(my_list, Ellipse, 1000)

random.shuffle(my_list)

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    for object in my_list:
        object.draw(screen, GREEN)
        object.move()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
