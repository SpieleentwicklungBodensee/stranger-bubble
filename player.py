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

    def setMaxx(self, x):
        self.maxx = int(x)

    def setMaxy(self, y):
        self.maxy = int(y)

    def go_up(self):
        if self.y == self.miny:
            self.status = "blocked"
        else:
            self.y = self.y - 1

    def go_down(self):
        if self.y == self.maxy:
            self.status = "blocked"
        else:
            self.y = self.y + 1

    def go_left(self):
        if self.x == self.minx:
            self.status = "blocked"
        else:
            self.x = self.x - 1

    def go_right(self):
        if self.x == self.maxx:
            self.status = "blocked"
        else:
            self.x = self.x + 1

    def getPlayerPosition(self):
        return self.x, self.y

    def getPlayerId(self):
        return self.id