class Player:
    pid = 1

    def __init__(self, name):
        self.pid = Player.pid
        self.name = name
        self.budget = 5
        self.game_lvl = 1
        self.hired_chara = []
        self.health = 4
        self.defeat_num = 0
        self.lvl_up_defeat = 2**self.game_lvl + 1
        Player.pid = Player.pid + 1

    def update(self):
        if self.defeat_num >= self.lvl_up_defeat:
            self.game_lvl = self.game_lvl + 1
            self.lvl_up_defeat = 2**self.game_lvl * 10
            return False
        else:
            return True
