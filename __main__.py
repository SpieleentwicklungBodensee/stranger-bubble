import pygame
from bitmapfont import BitmapFont

SCR_W = 320
SCR_H = 180

pygame.display.init()
screen = pygame.display.set_mode((SCR_W, SCR_H), flags=pygame.SCALED)

font = BitmapFont('gfx/heimatfont.png')



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


def update():
    pass


running = True

while running:
    render()
    controls()
    update()

pygame.quit()
