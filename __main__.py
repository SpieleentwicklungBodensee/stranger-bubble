import pygame
import threading
import socket
import pickle

from bitmapfont import BitmapFont
from player import Player
from keyItem import KeyItem

import network
import discover_server
import discover_client


SCR_W, SCR_H = 480, 270
TW, TH = 16, 16
LEV_W, LEV_H = 30, 17

CL_GAME_OVER = (200,12,12)
CL_BG_DARK = (16,6,26)
CL_TXT_PURPLE = (248,48,166)
CL_TXT_CYAN = (96,255, 250)

pygame.display.init()
screen = pygame.display.set_mode((SCR_W, SCR_H))#, flags=pygame.SCALED)

font = BitmapFont('gfx/heimatfont.png', scr_w=SCR_W, scr_h=SCR_H)
bigfont = BitmapFont('gfx/heimatfont.png', scr_w=SCR_W, scr_h=SCR_H, zoom=2)

tiles = {'#': pygame.image.load('gfx/wall.png'),
         ' ': pygame.image.load('gfx/floor.png'),
         'x': pygame.image.load('gfx/lava.png'),
         'O': pygame.image.load('gfx/overlay.png'),
         'd': pygame.image.load('gfx/door.png'),
         'f': pygame.image.load('gfx/door.png'),
         'a': pygame.image.load('gfx/key.png'),
         'b': pygame.image.load('gfx/cassette.png'),
         'c': pygame.image.load('gfx/coin.png'),
         '1': pygame.image.load('gfx/key.png'),
         '2': pygame.image.load('gfx/cassette.png'),
         '3': pygame.image.load('gfx/coin.png'),
         }

sprites = {'player1': pygame.image.load('gfx/man-green.png'),
           'player2': pygame.image.load('gfx/man-blue.png'),
           'p1d1': pygame.image.load('gfx/player1down1.png'),
           'p1d2': pygame.image.load('gfx/player1down2.png'),
           'p1d3': pygame.image.load('gfx/player1down3.png'),
           'p1d4': pygame.image.load('gfx/player1down4.png'),
           'p1u1': pygame.image.load('gfx/player1up1.png'),
           'p1u2': pygame.image.load('gfx/player1up2.png'),
           'p1u3': pygame.image.load('gfx/player1up3.png'),
           'p1u4': pygame.image.load('gfx/player1up4.png'),
           'p1r1': pygame.image.load('gfx/player1right1.png'),
           'p1r2': pygame.image.load('gfx/player1right2.png'),
           'p1r3': pygame.image.load('gfx/player1right3.png'),
           'p1r4': pygame.image.load('gfx/player1right4.png'),
           'p1l1': pygame.image.load('gfx/player1left1.png'),
           'p1l2': pygame.image.load('gfx/player1left2.png'),
           'p1l3': pygame.image.load('gfx/player1left3.png'),
           'p1l4': pygame.image.load('gfx/player1left4.png'),
           'p2d1': pygame.image.load('gfx/player2down1.png'),
           'p2d2': pygame.image.load('gfx/player2down2.png'),
           'p2d3': pygame.image.load('gfx/player2down3.png'),
           'p2d4': pygame.image.load('gfx/player2down4.png'),
           'p2u1': pygame.image.load('gfx/player2up1.png'),
           'p2u2': pygame.image.load('gfx/player2up2.png'),
           'p2u3': pygame.image.load('gfx/player2up3.png'),
           'p2u4': pygame.image.load('gfx/player2up4.png'),
           'p2r1': pygame.image.load('gfx/player2right1.png'),
           'p2r2': pygame.image.load('gfx/player2right2.png'),
           'p2r3': pygame.image.load('gfx/player2right3.png'),
           'p2r4': pygame.image.load('gfx/player2right4.png'),
           'p2l1': pygame.image.load('gfx/player2left1.png'),
           'p2l2': pygame.image.load('gfx/player2left2.png'),
           'p2l3': pygame.image.load('gfx/player2left3.png'),
           'p2l4': pygame.image.load('gfx/player2left4.png'),
           }


level_orig = ['##############################',
              '#      #      xx             #',
              '#     ad                     #',
              '#      #             xxx     #',
              '#   ####           xxxx      #',
              '#                            #',
              '#        xx    b       xx    #',
              '#  c  xxxx     xx            #',
              '########### ##################',
              '#                            #',
              '#           xx    123        #',
              '#    xx      x       ##f##   #',
              '#  xxxxx            xx       #',
              '#                    xxx     #',
              '#        xx                  #',
              '#                            #',
              '##############################',
              ]

level = list(level_orig)    # copy level


overlay1 = ['OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOO   OOO',
            'OOO   OOOOOOOOOOOOOOOOOO   OOO',
            'OOO   OOOOOO  OOOOOOOOOOOOOOOO',
            'OOOOOOOO  OO  OOOO  OOOOOOOOOO',
            'OOOOOOOO  OOOOOOOO  OOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOO  OOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOO  OOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            ]

overlay2 = ['                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            '                              ',
            'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOO  OOOOOO   OOOOOOOOO',
            'OOOO  OOOO  OOO  O   OOOOOOOOO',
            'OOOO  OOOOOOOOO  OOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOO   OOO',
            'OOOOOOOO  OOOOOOOOOOOOOO   OOO',
            'OOOOOOOO  OOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
            ]

def setTile(t, x, y):
    level[y] = level[y][:x] + t + level[y][x+1:]


class Screen:
    def __init__(self):
        pass

    def render(self):
        pass

    def keydown(self, key, shift=False):
        pass

    def keyup(self, key, shift=False):
        pass

    def update(self):
        pass

    def serverCallback(self, addr):
        pass

    def clientCallback(self):
        pass


class GameScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        global level
        level = list(level_orig)    # copy level

        self.player1 = Player('p1', 3, 3, LEV_W-2, LEV_H-2)
        self.player2 = Player('p2', 26, 13, LEV_W-2, LEV_H-2)
        self.player1.setStatusState('alive')
        self.player2.setStatusState('alive')

        if network.NETWORK_ROLE == 'server':
            self.curPlayer = self.player1
            self.currentOverlay = overlay1
        else:
            self.curPlayer = self.player2
            self.currentOverlay = overlay2

        self.keyItem1 = KeyItem('a', 'b', 'c', 'd')
        self.keyItem2 = KeyItem('1', '2', '3', 'f')
        #self.keyItem = self.keyItem1

        self.messages = []


    def render(self):
        screen.fill((0, 0, 0))

        for y, line in enumerate(level):
            for x, tile in enumerate(line):
                # draw actual tile
                screen.blit(tiles[tile], (x * TW, y * TH))

                #draw or hide keys
                for keyItem in (self.keyItem1, self.keyItem2):
                    if tile == keyItem.key1.getSym():
                        keyItem.setKey1Pos(x, y)
                        if keyItem.key1.getTaken() == True:
                            screen.blit(tiles[' '], (x * TW, y * TH))
                    if tile == keyItem.key2.getSym():
                        keyItem.setKey2Pos(x, y)
                        if keyItem.key2.getTaken() == True or keyItem.key1.getTaken() == False:
                            screen.blit(tiles[' '], (x * TW, y * TH))
                    if tile == keyItem.key3.getSym():
                        keyItem.setKey3Pos(x, y)
                        if keyItem.key3.getTaken() == True or keyItem.key2.getTaken() == False:
                            screen.blit(tiles[' '], (x * TW, y * TH))
                    if keyItem.getDoorState() != 'locked':
                        if tile == keyItem.getSymDoor():
                            setTile(' ', x, y)
                            network.sendTileChange(' ', x, y)

                # draw overlay
                if self.currentOverlay is not None:
                    if self.currentOverlay[y][x] != ' ':
                        screen.blit(tiles[self.currentOverlay[y][x]], (x * TW, y * TH))

        #draw player/s
        screen.blit(sprites[self.player1.getPlayerSpriteId()], (self.player1.getx() * TW, self.player1.gety() * TH))
        screen.blit(sprites[self.player2.getPlayerSpriteId()], (self.player2.getx() * TW, self.player2.gety() * TH))

    def keydown(self, key, shift=False):
        global running

        #current player
        if key in [pygame.K_a, pygame.K_LEFT]:
            self.curPlayer.go_left(level)

        if key in [pygame.K_d, pygame.K_RIGHT]:
            self.curPlayer.go_right(level)

        if key in [pygame.K_w, pygame.K_UP]:
            self.curPlayer.go_up(level)

        if key in [pygame.K_s, pygame.K_DOWN]:
            self.curPlayer.go_down(level)

        if key == pygame.K_F12:
            if shift:
                if self.currentOverlay is not None:
                    self.currentOverlay = None
                else:
                    self.currentOverlay = overlay1
            else:
                if self.currentOverlay == overlay1:
                    self.currentOverlay = overlay2
                else:
                    self.currentOverlay = overlay1

    def keyup(self, key, shift=False):
        global nextScreen

        if key == pygame.K_ESCAPE:
            nextScreen = TitleScreen()

    def update(self):
        self.proofEventPlayer()

        self.logicFortheKey(self.keyItem1)
        self.logicFortheKey(self.keyItem2)

        network.sendPosition(self.curPlayer.getPlayerPosition())
        network.sendKeyItemState(self.keyItem1)
        network.sendKeyItemState(self.keyItem2)

        self.processMessages()

    def serverCallback(self, data, addr):
        if addr != network.clientAddr:
            return

        #print('received: ', data)
        self.messages.append(data)

    def clientCallback(self, data):
        #print('received: ', data)
        self.messages.append(data)

    def processMessages(self):
        for data in list(self.messages):
            if data.startswith(b'PLAYER1_POS'):
                pos = data.split(b'=')[1]
                x, y = pos.split(b'/')

                self.player1.x = int(x)
                self.player1.y = int(y)

            elif data.startswith(b'PLAYER2_POS'):
                pos = data.split(b'=')[1]
                x, y = pos.split(b'/')

                self.player2.x = int(x)
                self.player2.y = int(y)

            elif data.startswith(b'KEYITEM1'):
                pickled = data.split(b'=')[1]
                self.keyItem1 = pickle.loads(pickled)

            elif data.startswith(b'KEYITEM2'):
                pickled = data.split(b'=')[1]
                self.keyItem2 = pickle.loads(pickled)

            elif data.startswith(b'TILECHANGE'):
                txy = data.split(b'=')[1]
                t, x, y = txy.split(b'/')
                setTile(t.decode('utf8'), int(x), int(y))

            elif data == b'GAMEOVER':
                self.gameoverHandler()

        self.messages.clear()

    def gameoverHandler(self):
        global nextScreen
        nextScreen = GameOverScreen()

    def proofEventPlayer(self):
        #proof is current player death, because of lava
        if 'x' == level[self.curPlayer.gety()][self.curPlayer.getx()]:
            if self.curPlayer.getStatusState() != 'death':
                self.curPlayer.setStatusState('death')
                print(" --- player state is : ", self.curPlayer.getStatusState(), ", because of the player lava dance.")
                self.gameoverHandler()
                network.sendGameOver()

    def logicFortheKey(self, keyItem):
        if keyItem.unlocked == False:
            if keyItem.key1.getTaken() == False:
                if self.curPlayer.getx() == keyItem.key1.getx() and self.curPlayer.gety() == keyItem.key1.gety():
                    keyItem.key1.setTaken(True)
            else:
                if keyItem.key2.getTaken() == False:
                    if self.curPlayer.getx() == keyItem.key2.getx() and self.curPlayer.gety() == keyItem.key2.gety():
                        keyItem.key2.setTaken(True)
                else:
                    if keyItem.key3.getTaken() == False:
                        if self.curPlayer.getx() == keyItem.key3.getx() and self.curPlayer.gety() == keyItem.key3.gety():
                            keyItem.key3.setTaken(True)
                    else:
                        keyItem.setDoorState('unlocked')


class GameOverScreen(Screen):
    def __init__(self):
        super().__init__()
        self.cursorY = 0
        self.r = 220
        self.g = 12
        self.b = 12

    def render(self):
        ##screen.fill(CL_GAME_OVER)
        screen.fill((self.r, self.g, self.b))
        if self.r > 0:
            self.r = self.r - 1
        bigfont.centerText(screen, 'GAME OVER', y=4, fgcolor=CL_TXT_PURPLE)
        font.centerText(screen, 'PRESS SPACE TO RESTART', y=20, fgcolor=(255, 255, 255))

    def keydown(self, key, shift=False):
        pass

    def keyup(self, key, shift=False):
        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            network.sendRestart()
            self.restartHandler()

        elif key == pygame.K_ESCAPE:
            global nextScreen
            nextScreen = TitleScreen()

            nextScreen.cursorY = 0

    def serverCallback(self, data, addr):
        if addr != network.clientAddr:
            return

        print('received: ', data)
        if data == b'RESTART':
            self.restartHandler()

    def clientCallback(self, data):
        print('received: ', data)

        if data == b'RESTART':
            self.restartHandler()

    def restartHandler(self):
        global nextScreen
        nextScreen = GameScreen()


class TitleScreen(Screen):
    def __init__(self):
        super().__init__()
        self.cursorY = 0

        self.menu = ['START GAME',
                     'JOIN GAME',
                     'EXIT',
                     ]

    def render(self):
        screen.fill(CL_BG_DARK)
        bigfont.centerText(screen, 'STRANGER BUBBLE', y=4, fgcolor=CL_TXT_PURPLE)

        for i, entry in enumerate(self.menu):
            font.centerText(screen, entry, y=18 + i * 2, fgcolor=CL_TXT_CYAN)

        if tick % 32 > 8:
            font.drawText(screen, '}', x=23, y=18 + self.cursorY * 2, fgcolor=CL_TXT_PURPLE)

    def keydown(self, key, shift=False):
        if key == pygame.K_DOWN:
            self.cursorY += 1
            self.cursorY %= len(self.menu)

        elif key == pygame.K_UP:
            self.cursorY -= 1
            self.cursorY %= len(self.menu)

    def keyup(self, key, shift=False):
        global nextScreen
        global running

        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            entry = self.menu[self.cursorY]

            if entry == 'START GAME':
                nextScreen = WaitScreen()
            elif entry == 'JOIN GAME':
                nextScreen = JoinScreen()
            elif entry == 'EXIT':
                running = False

        elif key == pygame.K_ESCAPE:
            running = False


class WaitScreen(Screen):
    def __init__(self):
        super().__init__()
        self.client = None
        self.discovering = True

        network.reset()
        network.initServer(port=6000, callback=self.serverCallback)

        def discover():
            while self.discovering:
                try:
                    client, data = discover_server.waitForClient()
                    if data == b'STRANGERBUBBLE':
                        self.client = client
                except socket.timeout:
                    pass
            print('stopped discover')

        thread = threading.Thread(target=discover)
        thread.start()

    def render(self):
        screen.fill(CL_BG_DARK)
        font.centerText(screen, 'WAITING FOR PLAYER 2...', y=8, fgcolor=CL_TXT_PURPLE)

        if self.client:
            font.centerText(screen, 'FOUND %s' % self.client[0], y=12)

        font.centerText(screen, 'SPACE = NO NETWORK', y=20, fgcolor=(255, 255, 255))
        font.centerText(screen, '! ONLY FOR TESTING !', y=22, fgcolor=(255, 255, 255))

    def keydown(self, key, shift=False):
        pass

    def keyup(self, key, shift=False):
        global nextScreen
        global running

        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            nextScreen = GameScreen()
            self.discovering = False
            network.shutdownServer()

        elif key == pygame.K_ESCAPE:
            nextScreen = TitleScreen()
            self.discovering = False
            network.shutdownServer()

    def update(self):
        pass

    def serverCallback(self, data, addr):
        global nextScreen
        print('received', data)

        if data == b'LETS GO!':
            nextScreen = GameScreen()
            self.discovering = False
            #network.serverCallback = nextScreen.serverCallback
            network.clientAddr = addr


class JoinScreen(Screen):
    def __init__(self):
        super().__init__()
        self.servers = set()
        self.discovering = True

        self.cursorY = 0

        network.reset()

        def discover():
            while self.discovering:
                try:
                    server = discover_client.findServer(b'STRANGERBUBBLE')
                    self.servers.add(server[1])
                except socket.timeout:
                    pass

        thread = threading.Thread(target=discover)
        thread.start()

    def render(self):
        screen.fill(CL_BG_DARK)
        font.centerText(screen, 'SCANNING FOR GAMES ON YOUR NETWORK...', y=8, fgcolor=CL_TXT_PURPLE)

        for i, server in enumerate(self.servers):
            font.centerText(screen, '%s' % server[0], y=12+i*2)

            if i == self.cursorY:
                if tick % 32 > 8:
                    font.drawText(screen, '}', x=18, y=12+i*2)

    def keydown(self, key, shift=False):
        if key == pygame.K_DOWN:
            self.cursorY += 1
            self.cursorY %= len(self.servers)

        elif key == pygame.K_UP:
            self.cursorY -= 1
            self.cursorY %= len(self.servers)

    def keyup(self, key, shift=False):
        global nextScreen
        global running

        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.servers:
                self.discovering = False
                nextScreen = GameScreen()
                network.initClient(list(self.servers)[self.cursorY][0], 6000, callback=nextScreen.clientCallback)

        elif key == pygame.K_ESCAPE:
            nextScreen = TitleScreen()
            self.discovering = False

    def update(self):
        pass

running = True
clock = pygame.time.Clock()
tick = 0

currentScreen = TitleScreen()
nextScreen = None


while running:
    # draw the current screen
    currentScreen.render()
    pygame.display.flip()

    # handle events in current screen
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYDOWN:
            shift = e.mod & pygame.KMOD_SHIFT
            currentScreen.keydown(e.key, shift=shift)

            if e.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

        elif e.type == pygame.KEYUP:
            shift = e.mod & pygame.KMOD_SHIFT
            currentScreen.keyup(e.key, shift=shift)

    # update the current screen
    currentScreen.update()

    # limit to 60 fps
    clock.tick(60)
    tick += 1

    # switch to next screen
    if nextScreen is not None:
        network.serverCallback = nextScreen.serverCallback
        network.clientCallback = nextScreen.clientCallback

        currentScreen = nextScreen
        nextScreen = None


if network.NETWORK_ROLE == 'server':
    network.shutdownServer()
else:
    network.shutdownClient()

pygame.quit()
