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
         }


level = ['####################',
         '#                  #',
         '#                  #',
         '#        xx        #',
         '#     xxxx         #',
         '#      xx          #',
         '#                  #',
         '#                  #',
         '#                  #',
         '#                  #',
         '####################',
         ]



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
