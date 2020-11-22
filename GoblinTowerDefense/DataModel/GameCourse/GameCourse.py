import pygame
from DataModel.GameCourse.Road import Road
from DataModel.Entity.Characters.Character import Character


class GameCourse:
    pos = (0, 0)
    size = (700, 500)
    road_width = 60
    roadsDef = (
        # (x, y, width, height)
        # road block 0
        (500, 0, road_width, 50),
        (500, 50, road_width, 50),
        # road block 1
        (390, 100, 60, road_width),
        (450, 100, 60, road_width),
        (510, 100, 50, road_width),
        # road block 2
        (330, 0, road_width, 50),
        (330, 50, road_width, 50),
        (330, 100, road_width, 60),
        # road block 3
        (60, 0, 55, road_width),
        (115, 0, 55, road_width),
        (170, 0, 55, road_width),
        (225, 0, 55, road_width),
        (280, 0, 55, road_width),
        # road block 4
        (60, 60, road_width, 60),
        (60, 120, road_width, 60),
        (60, 180, road_width, 60),
        # road block 5
        (60, 240, 60, road_width),
        (120, 240, 60, road_width),
        (180, 240, 60, road_width),
        (240, 240, 60, road_width),
        (300, 240, 60, road_width),
        (360, 240, 60, road_width),
        (420, 240, 60, road_width),
        (480, 240, 80, road_width),
        # road block 6
        (500, 300, road_width, 60),
        (500, 360, road_width, 60),
        # road block 7
        (0, 420, 60, road_width),
        (60, 420, 60, road_width),
        (120, 420, 60, road_width),
        (180, 420, 60, road_width),
        (240, 420, 60, road_width),
        (300, 420, 60, road_width),
        (360, 420, 60, road_width),
        (420, 420, 60, road_width),
        (480, 420, 60, road_width),
        (540, 420, 20, road_width)
    )
    # BLACK
    roadColor = (240, 210, 40)
    move_points = [
        # move point 0
        (roadsDef[0][0], (roadsDef[0][1] + roadsDef[0][3])),
        # move point 1
        (roadsDef[1][0] - road_width, (roadsDef[1][1])),
        # move point 2
        (roadsDef[2][0], roadsDef[2][1]),
        # move point 3
        (roadsDef[3][0], roadsDef[3][1]),
        # move point 4
        (roadsDef[4][0], (roadsDef[4][1] + roadsDef[4][3])),
        # move point 5
        (roadsDef[5][0] + roadsDef[5][2] - road_width, (roadsDef[5][1])),
        # move point 6
        (roadsDef[6][0], (roadsDef[6][1] + roadsDef[6][3])),
        # move point 7
        (roadsDef[7][0], (roadsDef[7][1]))
    ]

    def __init__(self, scrn):
        self.screen = scrn
        self.roads = pygame.sprite.Group()
        for roadDef in GameCourse.roadsDef:
            road = Road(GameCourse.roadColor, roadDef)
            self.roads.add(road)

    def render(self):
        self.roads.draw(self.screen)

    def occupy(self, new_chara):
        for road in self.roads:
            is_collided = pygame.sprite.collide_rect(new_chara, road)
            if is_collided:
                return is_collided
        return False
