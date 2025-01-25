import time

FD_NONE = 0
FD_RIGHT = 1
FD_DOWN = 2
FD_LEFT = 3
FD_UP = 4

class Player:
    def __init__(self, id="none", x=1, y=1, maxx=30, maxy=17, blocklist=['#']):
        self.spriteid = str(id)
        self.x = x
        self.y = y
        self.minx = 1
        self.miny = 1
        self.maxx = maxx
        self.maxy = maxy
        self.status = str(id)
        self.facing = FD_NONE
        self.blocklist = blocklist
        self.animcnt = 0
        self.animspeed = 5
        self.blocked = False

    def setMaxx(self, x):
        self.maxx = int(x)

    def setMaxy(self, y):
        self.maxy = int(y)

    def setStatusState(self, newstate):
        self.status = str(newstate)

    def getStatusState(self):
        return str(self.status)

    def go_up(self, level):
        self.facing = FD_UP
        self.animcnt = 4 * self.animspeed
        if self.y == self.miny:
            return -1
        else:
            nextField = level[self.y-1][self.x]
            if nextField in self.blocklist:
                self.blocked = True
                return -1
            else:
                self.blocked = False
                self.y = self.y - 1
                return 0

    def go_down(self, level):
        self.facing = FD_DOWN
        self.animcnt = 4 * self.animspeed
        if self.y == self.maxy:
            return -1
        else:
            nextField = level[self.y+1][self.x]
            if nextField in self.blocklist:
                self.blocked = True
                return -1
            else:
                self.blocked = False
                self.y = self.y + 1
                return 0

    def go_left(self, level):
        self.facing = FD_LEFT
        self.animcnt = 4 * self.animspeed
        if self.x == self.minx:
            return -1
        else:
            nextField = level[self.y][self.x-1]
            if nextField in self.blocklist:
                self.blocked = True
                return -1
            else:
                self.blocked = False
                self.x = self.x - 1
                return 0

    def go_right(self, level):
        self.facing = FD_RIGHT
        self.animcnt = 4 * self.animspeed
        if self.x == self.maxx:
            return -1
        else:
            nextField = level[self.y][self.x+1]
            if nextField in self.blocklist:
                self.blocked = True
                return -1
            else:
                self.blocked = False
                self.x = self.x + 1
                return 0

    def getPlayerPosition(self):
        return self.x, self.y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getOffsetAnimX(self):
        if self.animcnt == 0 or self.blocked:
            return 0
        b = 16
        step = (int(self.animcnt / self.animspeed) / b * ((4 * self.animcnt)) )
        if self.facing == FD_LEFT:
            return +step
        elif self.facing == FD_RIGHT:
            return -step

        return 0
    
    def getOffsetAnimY(self):
        if self.animcnt == 0 or self.blocked:
            return 0
        b = 16
        step = (int(self.animcnt / self.animspeed) / b * ((4 * self.animcnt)) )
        if self.facing == FD_UP:
            return  step
        elif self.facing == FD_DOWN:
            return -step

        return 0

    def getPlayerSpriteId(self):

        if self.animcnt > 0:
            self.animcnt -= 1

        sprite = str(self.spriteid)

        if self.facing == FD_RIGHT:
            sprite += "r"
        elif self.facing == FD_DOWN or self.facing == FD_NONE:
            sprite += "d"
        elif self.facing == FD_LEFT:
            sprite += "l"
        elif self.facing == FD_UP:
            sprite += "u"
        else:
            sprite += "d"

        sprite += str(int(self.animcnt / self.animspeed) + 1)

        return sprite
