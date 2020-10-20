import pygame
from DataModel.GameCourse.Road import Road


# ----- Declare colors


class GameCourse:
    pos = (0, 0)
    size = (700, 500)
    road_width = 60
    roadsDef = (
        (500, 0, road_width, 100),  # road block 0
        (390, 100, 170, road_width),  # road block 1
        (330, 0, road_width, 160),  # road block 2
        (60, 0, 270, road_width),  # road block 3
        (60, 60, road_width, 180),  # road block 4
        (60, 240, 500, road_width),  # road block 5
        (500, 300, road_width, 120),  # road block 6
        (0, 420, 560, road_width)  # road block 7
    )
    # BLACK
    roadColor = (240, 210, 40)
    move_points = [
        (roadsDef[0][0], (roadsDef[0][1] + roadsDef[0][3])),  # move point 0
        (roadsDef[1][0] - road_width, (roadsDef[1][1])),  # move point 1
        (roadsDef[2][0], roadsDef[2][1]),  # move point 2
        (roadsDef[3][0], roadsDef[3][1]),  # move point 3
        (roadsDef[4][0], (roadsDef[4][1] + roadsDef[4][3])),  # move point 4
        (roadsDef[5][0] + roadsDef[5][2] - road_width, (roadsDef[5][1])),  # move point 5
        (roadsDef[6][0], (roadsDef[6][1] + roadsDef[6][3])),  # move point 6
        (roadsDef[7][0], (roadsDef[7][1]))  # move point 7
    ]

    def __init__(self, scrn):
        self.screen = scrn
        self.roads = pygame.sprite.Group()
        for roadDef in GameCourse.roadsDef:
            road = Road(GameCourse.roadColor, roadDef)
            self.roads.add(road)

    def render(self):
        self.roads.draw(self.screen)
