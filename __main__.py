import pygame
from bitmapfont import BitmapFont


SCR_W, SCR_H = 320, 180
TW, TH = 16, 16
LEV_W, LEV_H = 20, 11

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

currentOverlay = overlay1


def render():
    screen.fill((40,60,80))

    font.centerText(screen, 'STRANGER BUBBLE', y=4)

    for y, line in enumerate(level):
        for x, tile in enumerate(line):
            # draw actual tile

            if tile == '#':
                screen.blit(tiles['#'], (x * TW, y * TH))

            if tile == ' ':
                screen.blit(tiles[' '], (x * TW, y * TH))

            if tile == 'x':
                screen.blit(tiles['x'], (x * TW, y * TH))

            # draw overlay
            if currentOverlay[y][x] != ' ':
                screen.blit(tiles[currentOverlay[y][x]], (x * 16, y * 16))


    pygame.display.flip()


def controls():
    events = pygame.event.get()

    global running, currentOverlay

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

            elif e.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

            elif e.key == pygame.K_F12:
                if currentOverlay == overlay1:
                    currentOverlay = overlay2
                else:
                    currentOverlay = overlay1


def update():
    pass


running = True
clock = pygame.time.Clock()

while running:
    render()
    controls()
    update()

    clock.tick(60)

pygame.quit()
