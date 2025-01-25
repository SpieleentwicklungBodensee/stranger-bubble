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
        self.walking = False
        self.facing = FD_NONE
        self.blocklist = blocklist
        self.last_time_walked = 0

    def setMaxx(self, x):
        self.maxx = int(x)

    def setMaxy(self, y):
        self.maxy = int(y)

    def setStatusState(self, newstate):
        self.status = str(newstate)

    def getStatusState(self):
        return str(self.status)

    def go_up(self, level, tick):
        self.facing = FD_UP
        self.walking = True
        self.last_time_walked = tick
        if self.y == self.miny:
            return -1
        else:
            nextField = level[self.y-1][self.x]
            if nextField in self.blocklist:
                return -1
            else:
                self.y = self.y - 1
                return 0

    def go_down(self, level, tick):
        self.facing = FD_DOWN
        self.walking = True
        self.last_time_walked = tick
        if self.y == self.maxy:
            return -1
        else:
            nextField = level[self.y+1][self.x]
            if nextField in self.blocklist:
                return -1
            else:
                self.y = self.y + 1
                return 0

    def go_left(self, level, tick):
        self.facing = FD_LEFT
        self.walking = True
        self.last_time_walked = tick
        if self.x == self.minx:
            return -1
        else:
            nextField = level[self.y][self.x-1]
            if nextField in self.blocklist:
                return -1
            else:
                self.x = self.x - 1
                return 0

    def go_right(self, level, tick):
        self.facing = FD_RIGHT
        self.walking = True
        self.last_time_walked = tick
        if self.x == self.maxx:
            return -1
        else:
            nextField = level[self.y][self.x+1]
            if nextField in self.blocklist:
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

    def getPlayerSpriteId(self, tick):

        if self.walking:
            if int(tick - self.last_time_walked) > 16:
                self.walking = False

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

        if self.walking:
            if int(time.time() * 1000) % 400 < 100:
                sprite += "1"
            elif 100 <= int(time.time() * 1000) % 400 < 200:
                sprite += "2"
            elif 200 <= int(time.time() * 1000) % 400 < 300:
                sprite += "3"
            else:
                sprite += "4"
        else:
            sprite += "1"

        return sprite
