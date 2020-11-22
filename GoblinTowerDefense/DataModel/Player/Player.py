import math


class Player:
    pid = 1

    def __init__(self, name):
        self.pid = Player.pid
        self.name = name
        self.budget = 5
        self.game_lvl = 1
        self.hired_chara = []
        self.health = 4
        self.num_to_defeat = 0
        self.lvl_up_defeat = self.game_lvl * 5
        Player.pid = Player.pid + 1

    def update(self):
        print(self.num_to_defeat, self.lvl_up_defeat)
        if self.num_to_defeat >= self.lvl_up_defeat:
            self.game_lvl = self.game_lvl + 1
            self.lvl_up_defeat = self.game_lvl * 5
            self.num_to_defeat = 0
            return False
        else:
            return True
