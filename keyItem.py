class KeyItem:
    def __init__(self, sym1, sym2, sym3):
        self.spriteid = str(id)
        self.doorState = 'locked'
        self.unlocked = False
        self.key1 = Keykey(0, 0, sym1)
        self.key2 = Keykey(0, 0, sym2)
        self.key3 = Keykey(0, 0, sym3)

    def getDoorState(self):
        return self.doorState
    
    def setDoorState(self, state):
        self.doorState = state
        if state == 'unlocked':
            self.unlocked = True
    
    def setKey1Pos(self, x, y):
        self.key1.setKeyPos(x, y)

    def setKey2Pos(self, x, y):
        self.key2.setKeyPos(x, y)

    def setKey3Pos(self, x, y):
        self.key3.setKeyPos(x, y)


class Keykey:
    def __init__(self, x, y, sym):
        self.x = x
        self.y = y
        self.sym = sym
        self.taken = False

    def setKeyPos(self, x, y):
        self.x = x
        self.y = y

    def setTaken(self, b):
        self.taken = b

    def getTaken(self):
        return self.taken
    
    def getx(self):
        return self.x
    
    def gety(self):
        return self.y
    
    def getSym(self):
        return self.sym   
    
