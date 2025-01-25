class Player:
    def __init__(self, id="none", x=1, y=1, maxx=30, maxy=17):
        self.spriteid = str(id)
        self.x = x
        self.y = y
        self.minx = 1
        self.miny = 1
        self.maxx = maxx
        self.maxy = maxy
        self.status = str(id)

    def setMaxx(self, x):
        self.maxx = int(x)

    def setMaxy(self, y):
        self.maxy = int(y)

    def setStatusState(self, newstate):
        self.status = str(newstate)

    def getStatusState(self):
        return str(self.status)

    def go_up(self, level):
        if self.y == self.miny:
            return -1
        else:
            nextField = level[self.y-1][self.x]
            if nextField in ['#', 'd']:
                return -1
            else:
                self.y = self.y - 1
                return 0

    def go_down(self, level):
        if self.y == self.maxy:
            return -1
        else:
            nextField = level[self.y+1][self.x]
            if nextField in ['#', 'd']:
                return -1
            else:
                self.y = self.y + 1
                return 0

    def go_left(self, level):
        if self.x == self.minx:
            return -1
        else:
            nextField = level[self.y][self.x-1]
            if nextField in ['#', 'd']:
                return -1
            else:
                self.x = self.x - 1
                return 0

    def go_right(self, level):
        if self.x == self.maxx:
            return -1
        else:
            nextField = level[self.y][self.x+1]
            if nextField in ['#', 'd']:
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
