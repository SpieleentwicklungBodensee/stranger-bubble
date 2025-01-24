class Player:
    def __init__(self, id, x=1, y=1):
        self.id = int(id)
        self.x = x
        self.y = y
        self.minx = 2
        self.miny = 2
        self.maxx = 480-2
        self.maxy = 270-2        
        self.status = "None"

    def setMaxx(x):
        Player.maxx = int(x)

    def setMaxy(y):
        Player.maxy = int(y)

    def go_up():
        if Player.y == Player.miny:
            Player.status = "blocked"
        else:
            Player.y = Player.y - 1

    def go_down():
        if Player.y == Player.maxy:
            Player.status = "blocked"
        else:
            Player.y = Player.y + 1

    def go_left():
        if Player.x == Player.minx:
            Player.status = "blocked"
        else:
            Player.x = Player.x - 1

    def go_right():
        if Player.x == Player.maxx:
            Player.status = "blocked"
        else:
            Player.x = Player.x + 1

    def getPlayerPosition():
        return Player.x, Player.y

    def getPlayerId():
        return Player.id