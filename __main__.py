import pygame
from bitmapfont import BitmapFont
from player import Player


SCR_W, SCR_H = 480, 270
TW, TH = 16, 16
LEV_W, LEV_H = 30, 17

CL_BG_DARK =(16,6,26)
CL_TXT_PURPLE = (248,48,166)


pygame.display.init()
screen = pygame.display.set_mode((SCR_W, SCR_H), flags=pygame.SCALED)

font = BitmapFont('gfx/heimatfont.png', scr_w=SCR_W, scr_h=SCR_H)
bigfont = BitmapFont('gfx/heimatfont.png', scr_w=SCR_W, scr_h=SCR_H, zoom=2)

tiles = {'#': pygame.image.load('gfx/wall.png'),
         ' ': pygame.image.load('gfx/floor.png'),
         'x': pygame.image.load('gfx/lava.png'),
         'O': pygame.image.load('gfx/overlay.png'),
         }

sprites = {'player1': pygame.image.load('gfx/man.png'),
           'player2': pygame.image.load('gfx/man.png'),
           }


level = ['##############################',
         '#             xx             #',
         '#                            #',
         '#                    xxx     #',
         '#                  xxxx      #',
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
        self.currentOverlay = overlay1
        self.player1 = Player('player1', 5, 5)
        self.player2 = Player('player2', 8, 8)


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
        self.player1.getPlayerSpriteId
        screen.blit(sprites[self.player1.getPlayerSpriteId], (self.player1.getx() * TW, self.player1.getx() * TH))
        screen.blit(sprites[self.player2.getPlayerSpriteId], (self.player2.getx() * TW, self.player2.getx() * TH))



    def keydown(self, key, shift=False):
        global running

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


class TitleScreen(Screen):
    def render(self):
        screen.fill(CL_BG_DARK)
        bigfont.centerText(screen, 'STRANGER BUBBLE', y=4, fgcolor=CL_TXT_PURPLE)
        font.centerText(screen, 'PRESS SPACE TO START', y=12, fgcolor=CL_TXT_PURPLE)

    def keyup(self, key, shift=False):
        global nextScreen
        global running

        if key == pygame.K_SPACE:
            nextScreen = GameScreen()

        elif key == pygame.K_ESCAPE:
            running = False


running = True
clock = pygame.time.Clock()

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

    # switch to next screen
    if nextScreen is not None:
        currentScreen = nextScreen
        nextScreen = None


pygame.quit()
