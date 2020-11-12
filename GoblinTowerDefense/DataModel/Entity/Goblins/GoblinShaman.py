from DataModel.Entity.Goblins.Goblin import Goblin
from DataModel.GameCourse.GameCourse import GameCourse


class GoblinShaman(Goblin):
    img_file = "Ext/characters/goblin_shaman.png"

    def __init__(self, pos, img_file, level):
        super().__init__(pos, img_file, level)
        self.speed = 10
        self.health = 15 * level
        self.defense = 0
        self.reward = 0.5
        self.point_to_move = GameCourse.move_points.copy()
