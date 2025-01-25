import pygame
import threading
import socket

from bitmapfont import BitmapFont
from player import Player

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
         }

sprites = {'player1': pygame.image.load('gfx/man-green.png'),
           'player2': pygame.image.load('gfx/man-blue.png'),
           }


level = ['##############################',
         '#             xx             #',
         '#                            #',
         '#      #             xxx     #',
         '#   ####           xxxx      #',
         '#                            #',
         '#        xx            xx    #',
         '#     xxxx     xx            #',
         '########### ##################',
         '#                            #',
         '#           xx               #',
         '#    xx      x               #',
         '#  xxxxx            xx       #',
         '#                    xxx     #',
         '#        xx                  #',
         '#                            #',
         '##############################',
         ]

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



class GameScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.player1 = Player('player1', 3, 3, LEV_W-2, LEV_H-2)
        self.player2 = Player('player2', 26, 13, LEV_W-2, LEV_H-2)
        self.player1.setStatusState('alive')
        self.player2.setStatusState('alive')

        if network.NETWORK_ROLE == 'server':
            self.curPlayer = self.player1
            self.currentOverlay = overlay1
        else:
            self.curPlayer = self.player2
            self.currentOverlay = overlay2

    def render(self):
        for y, line in enumerate(level):
            for x, tile in enumerate(line):
                # draw actual tile
                screen.blit(tiles[tile], (x * TW, y * TH))

                # draw overlay
                if self.currentOverlay is not None:
                    if self.currentOverlay[y][x] != ' ':
                        screen.blit(tiles[self.currentOverlay[y][x]], (x * TW, y * TH))

        #draw player/s
        screen.blit(sprites[self.player1.getPlayerSpriteId()], (self.player1.getx() * TW, self.player1.gety() * TH))
        screen.blit(sprites[self.player2.getPlayerSpriteId()], (self.player2.getx() * TW, self.player2.gety() * TH))
        self.proofEventPlayer()

    def proofEventPlayer(self):
        #proof is current player death, beacuse of lava
        if 'x' == level[self.curPlayer.gety()][self.curPlayer.getx()]:
            if self.curPlayer.getStatusState() != 'death':
                self.curPlayer.setStatusState('death')
                print(" --- player state is : ", self.curPlayer.getStatusState(), ", because of the player lava dance.")
                self.gameoverHandler()

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
        pass

    def gameoverHandler(self):
        global nextScreen
        nextScreen = GameOverScreen()


class GameOverScreen(Screen):
    def __init__(self):
        super().__init__()
        self.cursorY = 0
        self.r = 220
        self.g = 12
        self.b = 12
        self.bGoToMainMenue = False

    def render(self):
        ##screen.fill(CL_GAME_OVER)
        screen.fill((self.r, self.g, self.b))
        if self.r > 0:
            self.r = self.r - 1
        bigfont.centerText(screen, 'GAME OVER', y=4, fgcolor=CL_TXT_PURPLE)
        font.centerText(screen, 'PRESS SPACE fOR MAIN MENUE', y=20, fgcolor=(255, 255, 255))

    def keydown(self, key, shift=False):
        global nextScreen
        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            self.bGoToMainMenue = True

    def keyup(self, key, shift=False):
        global nextScreen
        if self.bGoToMainMenue == True:
            nextScreen = TitleScreen()
            nextScreen.cursorY = 0


    def serverCallback(self, data):
        print('received: ', data)

    def clientCallback(self, data):
        print('received: ', data)

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

        network.initServer(port=6000, callback=self.serverCallback)

        def discover():
            while self.discovering:
                try:
                    client, data = discover_server.waitForClient()
                    if data == b'STRANGERBUBBLE':
                        self.client = client
                except socket.timeout:
                    pass

        thread = threading.Thread(target=discover)
        thread.start()

    def render(self):
        screen.fill(CL_BG_DARK)
        font.centerText(screen, 'WAITING FOR PLAYER 2...', y=8, fgcolor=CL_TXT_PURPLE)

        if self.client:
            font.centerText(screen, 'FOUND %s:%s' % self.client, y=12)

        font.centerText(screen, 'PRESS SPACE TO SKIP', y=20, fgcolor=(255, 255, 255))

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

    def update(self):
        pass

    def serverCallback(self, data):
        global nextScreen
        print('received', data)

        if data == b'LETS GO!':
            nextScreen = GameScreen()
            self.discovering = False
            network.serverCallback = nextScreen.serverCallback


class JoinScreen(Screen):
    def __init__(self):
        super().__init__()
        self.servers = set()
        self.discovering = True

        self.cursorY = 0

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
            font.centerText(screen, '%s:%s' % server, y=12+i*2)

            if i == self.cursorY:
                if tick % 32 > 8:
                    font.drawText(screen, '}', x=3, y=12+i*2)

    def keydown(self, key, shift=False):
        pass

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
        currentScreen = nextScreen
        nextScreen = None


if network.NETWORK_ROLE == 'server':
    network.shutdownServer()
else:
    network.shutdownClient()

pygame.quit()
