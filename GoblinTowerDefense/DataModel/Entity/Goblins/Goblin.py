import math
from DataModel.Entity.Entity import Entity
from DataModel.GameCourse.GameCourse import GameCourse


class Goblin(Entity):
    size = (50, 50)
    img_file = "icons/characters/goblin.png"

    def __init__(self, pos):
        super().__init__(pos, Goblin.size, Goblin.img_file)
        self.speed = 5
        self.health = 5
        self.defense = 0
        self.reward = 5
        self.point_to_move = GameCourse.move_points.copy()

    def update(self):
        # Moving the goblins to the coordinates designed in GameCourse
        if len(self.point_to_move) > 0:
            diff_x = self.point_to_move[0][0] - self.rect.x
            diff_y = self.point_to_move[0][1] - self.rect.y

            angle = math.atan2(diff_x, diff_y)
            next_x = self.speed * math.sin(angle)
            next_y = self.speed * math.cos(angle)

            if (self.rect.x > self.point_to_move[0][0] - self.speed
                and self.rect.x < self.point_to_move[0][0] + self.speed) and (
                    self.rect.y > self.point_to_move[0][1] - self.speed
                    and self.rect.y < self.point_to_move[0][1] + self.speed):
                self.rect.x = self.point_to_move[0][0]
                self.rect.y = self.point_to_move[0][1]
                self.point_to_move.pop(0)
            else:
                self.rect.x = self.rect.x + math.floor(next_x)
                self.rect.y = self.rect.y + math.floor(next_y)
