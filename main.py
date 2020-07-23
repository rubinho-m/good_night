import os
import pygame
import pymorphy2
import sys

pygame.init()

size = (width, height) = 1920, 1080
cursor_size = (350, 350)
bear_size = (560, 400)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
HEAD_COLOR = (183, 175, 147)

FPS = 30

FONT = 'BalsamiqSans-BoldItalic.ttf'


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


def change_day_text(day, day_number):
    return f"МЕДВЕДЬ СПИТ {day_number} {day.make_agree_with_number(day_number).word.upper()}"


def start_game():
    running = True
    pygame.mouse.set_visible(False)
    morph = pymorphy2.MorphAnalyzer()
    day = morph.parse('день')[0]
    bg = pygame.transform.scale(load_image('bg.jpg'), (width, height))
    bear = pygame.transform.scale(load_image('bear.png'), bear_size)
    screen.blit(bg, (0, 0))
    screen.blit(bear, (width / 2, height / 2))
    pygame.draw.rect(screen, HEAD_COLOR, (0, 0, width, 0.2 * height))
    cursor = pygame.transform.scale(load_image('weapon.png'), cursor_size)
    noise = 0
    step = 10
    font = pygame.font.Font(FONT, 35)
    day_number = 1
    line = f"МЕДВЕДЬ СПИТ {day_number} {day.make_agree_with_number(day_number).word.upper()}"
    string_rendered = font.render(line, 6, pygame.Color('black'))
    screen.blit(string_rendered, (width / 2, height / 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    noise += step
                    day_number += 1
                    line = change_day_text(day, day_number)
                    string_rendered = font.render(line, 6, pygame.Color('black'))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()

        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            screen.blit(cursor, pos)

        pygame.display.flip()
        screen.blit(bg, (0, 0))
        screen.blit(bear, (width / 2, height / 2))
        pygame.draw.rect(screen, HEAD_COLOR, (0, 0, width, 0.185 * height))
        screen.blit(string_rendered, (0.4 * width, 0.13 * height))
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
