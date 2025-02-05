import pygame
import threading
import socket
import pickle
import random
import string
import time

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

try:
    import settings
    displayflags = 0

    if hasattr(settings, 'DEBUG_MODE'):
        DEBUG_MODE = settings.DEBUG_MODE
    else:
        DEBUG_MODE = False

    if hasattr(settings, 'FULLSCREEN'):
        if settings.FULLSCREEN:
            displayflags |= pygame.FULLSCREEN

    if hasattr(settings, 'SCALED'):
        if settings.SCALED:
            displayflags |= pygame.SCALED
    else:
        displayflags |= pygame.SCALED

    if hasattr(settings, 'NETWORK_NAME'):
        networkName = str(settings.NETWORK_NAME)[:16].upper()
    else:
        networkName = None
except:
    displayflags = pygame.SCALED
    networkName = None
    DEBUG_MODE = False

pygame.display.init()
screen = pygame.display.set_mode((SCR_W, SCR_H), flags=displayflags)

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
         'g': pygame.image.load('gfx/overlay_tl.png'),
         'h': pygame.image.load('gfx/overlay_t.png'),
         'i': pygame.image.load('gfx/overlay_tr.png'),
         'j': pygame.image.load('gfx/overlay_l.png'),
         'k': pygame.image.load('gfx/overlay_r.png'),
         'l': pygame.image.load('gfx/overlay_bl.png'),
         'm': pygame.image.load('gfx/overlay_b.png'),
         'n': pygame.image.load('gfx/overlay_br.png'),
         'o': pygame.image.load('gfx/mine_overlay.png'),  #player 2
         'p': pygame.image.load('gfx/mine_overlay.png'),  #player 1
         'q': pygame.image.load('gfx/bubble1.png'),  #<<<< super bubble button player 1  Xq
         'r': pygame.image.load('gfx/bubble1.png'),  #<<<< super bubble button player 2
         's': pygame.image.load('gfx/gate.png'),  #<<<< super bubble mine player 1
         't': pygame.image.load('gfx/gate.png'),  #<<<< super bubble mine player 2       Xt
         'u': pygame.image.load('gfx/gate.png'),
         'V': pygame.image.load('gfx/bubble3.png'),
         'W': pygame.image.load('gfx/bubble4.png'),
         }

alphatiles = {}
for t in tiles.keys():
    alphatiles[t] = tiles[t].copy()
    alphatiles[t].convert()
    alphatiles[t].set_alpha(168)

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
              '#q o   #o     xx      o      #',
              '#   o a  t #     ##       o  #',
              '# #  t #   #t#t#t#   xxx     #',
              '#  #####   #   #   xxxx    o #',
              '#        o  #        #   o   #',
              '# #o###  xx #  b   # # #d#x  #',
              '#  c  xxxx  t  xx   #  #  #  #',
              '############        ###   ####',
              '#     p1s  ######    #       #',
              '#p  ######  xx  #######f##   #',
              '#    xx  #x  xx  x   #   #####',
              '# pxxxxx        xx   xx     x#',
              '#      ##   ###      xxx     #',
              '# p2 x   xx ###   ##s     p  #',
              '#    xx          #    pp  3 r#',
              '##############################',
              ]

level = list(level_orig)    # copy level


overlay1 = ['OOOOOOOOOOOghhhhhhiOOOOOOOOOOO',
            'OOghhhhhiOOj      kOOghhhhhiOO',
            'OOj     kOOj      kOOj     kOO',
            'OOj     kOOj      kOOj     kOO',
            'OOj     kOOj      kOOj     kOO',
            'OOlmmmmmnOOj      kOOlmmmmmnOO',
            'OOOOOOOOOOOj      kOOOOOOOOOOO',
            'hhhhhhiOOOOlmmmmmmnOOOOghhhhhh',
            '      kOOOOOOOOOOOOOOOOj      ',
            '       hhhhhhhhhhhhhhhh       ',
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
            '       mmmmmmmmmmmmmmmm       ',
            '      kOOOOOOOOOOOOOOOOj      ',
            'mmmmmmnOOOOghhhhhhiOOOOlmmmmmm',
            'OOOOOOOOOOOj      kOOOOOOOOOOO',
            'OOghhhhhiOOj      kOOghhhhhiOO',
            'OOj     kOOj      kOOj     kOO',
            'OOj     kOOj      kOOj     kOO',
            'OOj     kOOj      kOOj     kOO',
            'OOlmmmmmnOOj      kOOlmmmmmnOO',
            'OOOOOOOOOOOlmmmmmmnOOOOOOOOOOO',
            ]

global key1MsgCounter
global key2MsgCounter
global key3MsgCounter
key1MsgCounter = 0
key2MsgCounter = 0
key3MsgCounter = 0


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

    def serverCallback(self, data, addr):
        pass

    def clientCallback(self, data):
        pass


class GameScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        global level
        level = list(level_orig)    # copy level

        self.player1 = Player('p1', 3, 3, LEV_W-2, LEV_H-2, ['#', 'd', 'f'])
        self.player2 = Player('p2', 26, 13, LEV_W-2, LEV_H-2, ['#', 'd', 'f'])
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

        self.messages = []


    def render(self):
        screen.fill((0, 0, 0))

        for y, line in enumerate(level):
            for x, tile in enumerate(line):
                # draw actual tile
                if tile in ['o', 'p']:
                    screen.blit(tiles[' '], (x * TW, y * TH))
                else:
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

                if self.curPlayer is self.player1:
                    if tile == 'p':
                        screen.blit(tiles[' '], (x * TW, y * TH))
                    if tile == 'o':
                        screen.blit(tiles['o'], (x * TW, y * TH))


                if self.curPlayer is self.player2:
                    if tile == 'o':
                        screen.blit(tiles[' '], (x * TW, y * TH))
                    if tile == 'p':
                        screen.blit(tiles['p'], (x * TW, y * TH))

                if tile == 't':
                    if self.keyItem2.getSuperBubble() == True:
                        screen.blit(tiles[' '], (x * TW, y * TH))

                if tile == 's':
                    if self.keyItem1.getSuperBubble() == True:
                        screen.blit(tiles[' '], (x * TW, y * TH))


        #draw player/s
        screen.blit(sprites[self.player1.getPlayerSpriteId()], (self.player1.getx() * TW + self.player1.getOffsetAnimX(), self.player1.gety() * TH + self.player1.getOffsetAnimY()))
        screen.blit(sprites[self.player2.getPlayerSpriteId()], (self.player2.getx() * TW + self.player2.getOffsetAnimX(), self.player2.gety() * TH + self.player2.getOffsetAnimY()))

        # draw overlay again, but with alpha transparency
        for y, line in enumerate(level):
            for x, tile in enumerate(line):
                if self.currentOverlay is not None:
                    if self.currentOverlay[y][x] != ' ':
                        screen.blit(alphatiles[self.currentOverlay[y][x]], (x * TW, y * TH), special_flags=pygame.BLEND_ALPHA_SDL2)

        #draw key taken info
        global key1MsgCounter
        global key2MsgCounter
        global key3MsgCounter

        if key1MsgCounter > 0:
            key1MsgCounter = key1MsgCounter - 1
            font.centerText(screen, 'KEY ONE TAKEN', y=4, fgcolor=CL_TXT_CYAN)

        if key2MsgCounter > 0:
            key2MsgCounter = key2MsgCounter - 1
            font.centerText(screen, 'KEY TWO TAKEN - DOORS HALF UNLOCKED', y=4, fgcolor=CL_TXT_CYAN)

        if key3MsgCounter > 0:
            key3MsgCounter = key3MsgCounter - 1
            bigfont.centerText(screen, 'DOOR UNLOCKED', y=4, fgcolor=CL_TXT_CYAN)


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

        if key == pygame.K_F12 and DEBUG_MODE:
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

        if self.curPlayer == self.player1:
            network.sendPlayerState(self.player1)
            network.sendKeyItemState(self.keyItem1)
        else:
            network.sendPlayerState(self.player2)
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
            if data.startswith(b'PLAYER1_POS'): # deprecated
                pos = data.split(b'=')[1]
                x, y = pos.split(b'/')

                self.player1.x = int(x)
                self.player1.y = int(y)

            elif data.startswith(b'PLAYER2_POS'): # deprecated
                pos = data.split(b'=')[1]
                x, y = pos.split(b'/')

                self.player2.x = int(x)
                self.player2.y = int(y)

            elif data.startswith(b'PLAYER1'):
                pickled = data.split(b'=')[1]
                self.player1 = pickle.loads(pickled)

            elif data.startswith(b'PLAYER2'):
                pickled = data.split(b'=')[1]
                self.player2 = pickle.loads(pickled)

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
        if self.curPlayer.getStatusState() == 'death':
            self.gameoverHandler()
            network.sendGameOver()

        #proof is current player death, because of lava
        if level[self.curPlayer.gety()][self.curPlayer.getx()] in ['x', 'o', 'p']:
            if self.curPlayer.getStatusState() != 'deathanim' and self.curPlayer.getStatusState() != 'death':
                self.curPlayer.setStatusState('deathanim')
                #print(" --- player state is : ", self.curPlayer.getStatusState(), ", because of the player lava dance.")

        if self.player1.getx() == self.player2.getx() and self.player1.gety() == self.player2.gety():
            global nextScreen
            self.currentOverlay = None
            nextScreen = GameWinScreen()

        if self.curPlayer == self.player1:
            if level[self.curPlayer.gety()][self.curPlayer.getx()] in ['q']:
                self.keyItem1.setSuperBubble(True)
            else:
                self.keyItem1.setSuperBubble(False)


        if self.curPlayer == self.player2:
            if level[self.curPlayer.gety()][self.curPlayer.getx()] in ['r']:
                self.keyItem2.setSuperBubble(True)
            else:
                self.keyItem2.setSuperBubble(False)
        #action
        if self.keyItem2.getSuperBubble() == False:
            if level[self.player1.gety()][self.player1.getx()] in ['s','t'] and self.curPlayer.getStatusState() != 'deathanim' and self.curPlayer.getStatusState() != 'death':
                self.curPlayer.setStatusState('deathanim')

        if self.keyItem1.getSuperBubble() == False:
            if level[self.player2.gety()][self.player2.getx()] in ['s','t'] and self.curPlayer.getStatusState() != 'deathanim' and self.curPlayer.getStatusState() != 'death':
                self.curPlayer.setStatusState('deathanim')

    def logicFortheKey(self, keyItem):
        global key1MsgCounter
        global key2MsgCounter
        global key3MsgCounter
        maxMsgDelayTime = 240
        if keyItem.unlocked == False:
            if keyItem.key1.getTaken() == False:
                if self.curPlayer.getx() == keyItem.key1.getx() and self.curPlayer.gety() == keyItem.key1.gety():
                    keyItem.key1.setTaken(True)
                    key1MsgCounter = maxMsgDelayTime
            else:
                if keyItem.key2.getTaken() == False:
                    if self.curPlayer.getx() == keyItem.key2.getx() and self.curPlayer.gety() == keyItem.key2.gety():
                        keyItem.key2.setTaken(True)
                        key2MsgCounter = maxMsgDelayTime
                else:
                    if keyItem.key3.getTaken() == False:
                        if self.curPlayer.getx() == keyItem.key3.getx() and self.curPlayer.gety() == keyItem.key3.gety():
                            keyItem.key3.setTaken(True)
                            key3MsgCounter = maxMsgDelayTime
                    else:
                        keyItem.setDoorState('unlocked')


class GameWinScreen(Screen):
    def __init__(self):
        super().__init__()
        self.cursorY = 0
        self.r = 12
        self.g = 172
        self.b = 12
        self.winEndCounter = 180

    def render(self):
        if self.winEndCounter > 0:
            self.winEndCounter = self.winEndCounter -1
            bigfont.centerText(screen, 'CONGRATULATIONS!', y=4, fgcolor=CL_TXT_CYAN)
        else:
            screen.fill((self.r, self.g, self.b))
            if self.g > 68:
                self.g = self.g - 1
            bigfont.centerText(screen, 'YOU ARE A WINNER TYPE', y=4, fgcolor=CL_TXT_CYAN)
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
                     'HOW TO PLAY',
                     'EXIT',
                     ]

    def render(self):
        screen.fill(CL_BG_DARK)
        bigfont.centerText(screen, 'STRANGER BUBBLE', y=2.5, fgcolor=CL_TXT_PURPLE)

        if int(time.time() * 1000) % 1000 < 250:
            screen.blit(sprites['p1d2'], (240 - TW, 88))
            screen.blit(sprites['p2d1'], (240, 88))
        elif 100 <= int(time.time() * 1000) % 1000 < 500:
            screen.blit(sprites['p1d3'], (240 - TW, 88))
            screen.blit(sprites['p2d2'], (240, 88))
        elif 200 <= int(time.time() * 1000) % 1000 < 750:
            screen.blit(sprites['p1d4'], (240 - TW, 88))
            screen.blit(sprites['p2d3'], (240, 88))
        elif 300 <= int(time.time() * 1000) % 1000 < 1000:
            screen.blit(sprites['p1d1'], (240 - TW, 88))
            screen.blit(sprites['p2d4'], (240, 88))

        font.centerText(screen, 'BY BUSYBEAVER, MCMURC, ZEHA', y=27, fgcolor=CL_TXT_PURPLE)
        font.centerText(screen, 'GLOBAL GAMEJAM 2025', y=29, fgcolor=CL_TXT_PURPLE)

        for i, entry in enumerate(self.menu):
            font.centerText(screen, entry, y=16 + i * 2, fgcolor=CL_TXT_CYAN)

        if tick % 32 > 8:
            font.drawText(screen, '}', x=22, y=16 + self.cursorY * 2, fgcolor=CL_TXT_PURPLE)

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
            elif entry == 'HOW TO PLAY':
                nextScreen = HowtoScreen()
            elif entry == 'EXIT':
                running = False

        elif key == pygame.K_ESCAPE:
            running = False


class WaitScreen(Screen):
    def __init__(self):
        super().__init__()
        self.clients = set()
        self.discovering = True

        network.reset()
        network.initServer(port=6000, callback=self.serverCallback)

        if networkName:
            self.coolRandomName = networkName
        else:
            self.coolRandomName = ''.join(random.choices(string.ascii_uppercase, k=4))

        def discover():
            discover_server.init()
            while self.discovering:
                try:
                    client, data = discover_server.waitForClient(self.coolRandomName)
                    if data == b'STRANGERBUBBLE':
                        self.clients.add(client[0])
                except socket.timeout:
                    pass
            discover_server.shutdown()

        thread = threading.Thread(target=discover)
        thread.start()

    def render(self):
        screen.fill(CL_BG_DARK)
        bigfont.centerText(screen, self.coolRandomName, y=2, fgcolor=CL_TXT_CYAN)
        font.centerText(screen, 'WAITING FOR PLAYER 2...', y=8, fgcolor=CL_TXT_PURPLE)

        for i, client in enumerate(self.clients):
            font.centerText(screen, '%s ASKED...' % client, y=12+i*2)

        if DEBUG_MODE:
            font.centerText(screen, 'SPACE = NO NETWORK', y=20, fgcolor=(255, 255, 255))
            font.centerText(screen, '! ONLY FOR TESTING !', y=22, fgcolor=(255, 255, 255))

    def keydown(self, key, shift=False):
        pass

    def keyup(self, key, shift=False):
        global nextScreen
        global running

        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER) and DEBUG_MODE:
            nextScreen = GameScreen()
            self.discovering = False
            discover_server.shutdown()
            network.shutdownServer()

        elif key == pygame.K_ESCAPE:
            nextScreen = TitleScreen()
            self.discovering = False
            discover_server.shutdown()
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
            discover_client.init()
            while self.discovering:
                try:
                    server = discover_client.findServer(b'STRANGERBUBBLE')
                    self.servers.add(server) # coolRandomName, serverAddress
                except socket.timeout:
                    pass
            discover_client.shutdown()

        thread = threading.Thread(target=discover)
        thread.start()

    def render(self):
        screen.fill(CL_BG_DARK)
        font.centerText(screen, 'SCANNING FOR GAMES ON YOUR NETWORK...', y=8, fgcolor=CL_TXT_PURPLE)

        for i, server in enumerate(self.servers):
            coolRandomName = server[0].decode('utf8')
            serverName = server[1][0]
            font.drawText(screen, coolRandomName, x=20, y=12+i*2, fgcolor=CL_TXT_CYAN)
            font.drawText(screen, serverName, x=21 + len(coolRandomName), y=12+i*2, fgcolor=CL_TXT_PURPLE)

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
                discover_client.shutdown()
                nextScreen = GameScreen()

                coolRandomName, server = list(self.servers)[self.cursorY]
                network.initClient(server[0], 6000, callback=nextScreen.clientCallback)

        elif key == pygame.K_ESCAPE:
            nextScreen = TitleScreen()
            self.discovering = False
            discover_client.shutdown()

    def update(self):
        pass


class HowtoScreen(Screen):
    def __init__(self):
        super().__init__()

    def render(self):
        screen.fill(CL_BG_DARK)
        bigfont.centerText(screen, 'INSTRUCTIONS', y=1, fgcolor=CL_TXT_PURPLE)

        font.centerText(screen, 'THIS IS A COOP GAME FOR TWO PLAYERS', y=7, fgcolor=CL_TXT_CYAN)
        font.centerText(screen, '')
        font.centerText(screen, 'THE AIM OF THE GAME IS FOR BOTH PLAYERS TO MEET')
        font.centerText(screen, '')
        font.centerText(screen, 'HOWEVER, EACH PLAYER LIVES IN HIS OWN BUBBLE')
        font.centerText(screen, 'AND HAS LIMITED INFORMATION ABOUT HIS SURROUNDINGS')
        font.centerText(screen, '')
        font.centerText(screen, 'THUS, YOU SOMETIMES HAVE TO ASK YOUR CO-PLAYER')
        font.centerText(screen, 'IF IT\'S SAFE FOR YOU TO WALK ACROSS')
        font.centerText(screen, '')
        font.centerText(screen, 'STEPPING INTO LAVA    IS AN UNHEALTHY IDEA')
        font.centerText(screen, '')
        font.centerText(screen, 'DOORS    ARE OPENED BY COLLECTING THREE KEYS       ')
        font.centerText(screen, '')
        font.centerText(screen, 'DEADLY SKULLS    CAN NOT BE SEEN BY YOUR CO-PLAYER')
        font.centerText(screen, '')
        font.centerText(screen, 'MINES    CAN BE TEMPORARILY DEACTIVATED IF')
        font.centerText(screen, '')
        font.centerText(screen, 'THE CO-PLAYER STEPS ON THE MAGIC BUBBLE   ')
        font.centerText(screen, '')
        font.centerText(screen, '')
        font.centerText(screen, 'HAVE FUN!', fgcolor=CL_TXT_PURPLE)
        font.centerText(screen, '')
        font.centerText(screen, 'PRESS A KEY', fgcolor=CL_TXT_PURPLE)

        font.drawText(screen, 'BOTH PLAYERS TO MEET', x=33.5, y=9, fgcolor=CL_TXT_PURPLE)

        screen.blit(tiles['x'], (224, 132))

        screen.blit(tiles['d'], (84, 148))
        screen.blit(tiles['1'], (392, 148))
        screen.blit(tiles['2'], (392+16, 148))
        screen.blit(tiles['3'], (392+16+16, 148))

        screen.blit(tiles['o'], (152, 162))

        screen.blit(tiles['s'], (120, 180))
        screen.blit(tiles['q'], (390, 196))

    def keydown(self, key, shift=False):
        pass

    def keyup(self, key, shift=False):
        global nextScreen
        if key != pygame.K_F11:
            nextScreen = TitleScreen()

    def update(self):
        pass

    def serverCallback(self, data, addr):
        pass

    def clientCallback(self, data):
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
