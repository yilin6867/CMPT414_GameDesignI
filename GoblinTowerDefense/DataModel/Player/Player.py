class Player():
    pid = 1
    def __init__(self, name):
        self.pid = Player.pid
        self.name = name
        self.budget = 1000
        self.game_lvl = 1
        self.hired_chara = []
        self.health = 4
        Player.pid = Player.pid +1

