import pygame
from bitmapfont import BitmapFont

SCR_W = 320
SCR_H = 180

pygame.display.init()
screen = pygame.display.set_mode((SCR_W, SCR_H), flags=pygame.SCALED)

font = BitmapFont('gfx/heimatfont.png')

tiles = {'#': pygame.image.load('gfx/wall.png'),
         ' ': pygame.image.load('gfx/floor.png'),
         'x': pygame.image.load('gfx/lava.png'),
         'O': pygame.image.load('gfx/overlay.png'),
         }


level = ['####################',
         '#             xx   #',
         '#                  #',
         '#        xx        #',
         '#     xxxx     xx  #',
         '########### ########',
         '#           xx     #',
         '#    xx      x     #',
         '#  xxxxx           #',
         '#                  #',
         '####################',
         ]

overlay1 = ['OOOOOOOOOOOOOOOOOOOO',
            'O   OOOOOOOOOOOOOOOO',
            'O   OOOOOO  OOOOOOOO',
            'OOOOOO  OO  OOOO  OO',
            'OOOOOO  OOOOOOOO  OO',
            'OOOOOOOOOOOOOOOOOOOO',
            '                    ',
            '                    ',
            '                    ',
            '                    ',
            '                    ',
            ]

overlay2 = ['                    ',
            '                    ',
            '                    ',
            '                    ',
            '                    ',
            'OOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOO  OOOOOO   O',
            'OO  OOOO  OOO  O   O',
            'OO  OOOOOOOOO  OOOOO',
            'OOOOOOOOOOOOOOOOOOOO',
            ]


def render():
    screen.fill((40,60,80))

    font.centerText(screen, 'STRANGER BUBBLE', y=4)

    pygame.display.flip()


def controls():
    events = pygame.event.get()

    global running

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

            elif e.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()


def update():
    pass


running = True

while running:
    render()
    controls()
    update()

pygame.quit()
