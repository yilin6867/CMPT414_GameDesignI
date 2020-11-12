from DataModel.Entity.Goblins.Goblin import Goblin
from DataModel.GameCourse.GameCourse import GameCourse


class GoblinLord(Goblin):
    img_file = "Ext/characters/goblin_lord.png"

    def __init__(self, pos, img_file, level):
        super().__init__(pos, img_file, level)
        self.speed = 5
        self.health = 25 * level
        self.defense = 0
        self.reward = 2
        self.point_to_move = GameCourse.move_points.copy()
