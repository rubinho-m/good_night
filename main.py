from game_classes import Fly
import pygame
import pymorphy2
import random
import sys

pygame.init()

size = (width, height) = 1920, 1080
cursor_size = (350, 350)
bear_size = (560, 400)
min_progress_line_len = 50
max_progress_line_len = 450
full_progress_line_size = (min_progress_line_len, 50)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill(pygame.Color('black'))

HEAD_COLOR = (183, 175, 147)
PROGRESS_LINE_LIGHT = (0, 178, 155)
PROGRESS_LINE_DARK = (0, 110, 95)

FPS = 30
clock = pygame.time.Clock()

FONT = 'BalsamiqSans-BoldItalic.ttf'


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    # fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(name)
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

    dark_progress_line_cf = 1
    noise = 0
    step = 10
    day_number = 1
    all_fly_count = 0
    cool_down = 1000

    bear_delta_x, bear_delta_y = 185, 100
    weapon_delta_x, weapon_delta_y = 135, 100

    flies = []

    FLY_EVENT = 30
    pygame.time.set_timer(FLY_EVENT, cool_down)

    font = pygame.font.Font(FONT, 35)
    line = f"МЕДВЕДЬ СПИТ {day_number} {day.make_agree_with_number(day_number).word.upper()}"
    string_rendered = font.render(line, 6, pygame.Color('black'))

    screen.blit(string_rendered, (width / 2, height / 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == FLY_EVENT:
                vector = random.choice(['right', 'left'])
                if vector == 'right':
                    fly_pos = [random.randint(0, width // 2),
                               random.randint(height * 0.8, height)]
                else:
                    fly_pos = [random.randint(width // 2, width),
                               random.randint(height * 0.8, height)]
                flies.append(Fly(fly_pos, 60, 60, vector))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    noise += step
                    day_number += 1

                    dark_progress_line_cf -= 0.1
                    if dark_progress_line_cf < 0:
                        dark_progress_line_cf = 0

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

        for fly in flies:
            fly.move(screen)
            if fly.pos[0] > width + fly.width or fly.pos[0] < -fly.width:
                flies.remove(fly)

        pygame.draw.rect(screen, HEAD_COLOR, (0, 0, width, 0.185 * height))
        pygame.draw.rect(screen,
                         PROGRESS_LINE_LIGHT,
                         (1250,
                          0.125 * height,
                          full_progress_line_size[0],
                          full_progress_line_size[1]))
        pygame.draw.rect(screen,
                         PROGRESS_LINE_DARK,
                         (1250,
                          0.125 * height,
                          full_progress_line_size[0] * dark_progress_line_cf,
                          full_progress_line_size[1]))
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
