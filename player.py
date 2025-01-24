class Player:
    def __init__(self, id="None", x=1, y=1, maxx=29, maxy=16):
        self.spriteid = str(id)
        self.x = x
        self.y = y
        self.minx = 2
        self.miny = 2
        self.maxx = maxx
        self.maxy = maxy    
        self.status = "None"

    def setMaxx(self, x):
        self.maxx = int(x)

    def setMaxy(self, y):
        self.maxy = int(y)

    def go_up(self):
        if self.y == self.miny:
            self.status = "blocked"
            return -1
        else:
            self.y = self.y - 1
            return 0

    def go_down(self):
        if self.y == self.maxy:
            self.status = "blocked"
            return -1
        else:
            self.y = self.y + 1
            return 0

    def go_left(self):
        if self.x == self.minx:
            self.status = "blocked"
            return -1
        else:
            self.x = self.x - 1
            return 0

    def go_right(self):
        if self.x == self.maxx:
            self.status = "blocked"
            return -1
        else:
            self.x = self.x + 1
            return 0

    def getPlayerPosition(self):
        return self.x, self.y
    
    def getx(self):
        return self.x
    
    def gety(self):
        return self.y    

    def getPlayerSpriteId(self):
        return str(self.spriteid)