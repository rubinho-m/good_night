import os
import pygame
import sys

pygame.init()

size = (width, height) = 1920, 1080
cursor_size = (350, 350)
bear_size = (560, 400)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()

FPS = 30


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    pass


def start_menu():
    pass


def start_game():
    running = True
    pygame.mouse.set_visible(False)
    bg = pygame.transform.scale(load_image('bg.jpg'), (width, height))
    screen.blit(bg, (0, 0))
    cursor = pygame.transform.scale(load_image('weapon.png'), cursor_size)
    bear = pygame.transform.scale(load_image('bear.png'), bear_size)
    noise = 0
    step = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    noise += step

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()

        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            screen.blit(cursor, pos)

        pygame.display.flip()
        screen.blit(bg, (0, 0))
        screen.blit(bear, (width / 2, height / 2))
        clock.tick(FPS)


GREETING = 0
MENU = 1
GAME = 2

todo = {GREETING: start_screen,
        MENU: start_menu,
        GAME: start_game}

state = GAME

while True:
    state = todo[state]()
