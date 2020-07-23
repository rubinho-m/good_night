import pygame
import random

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


class Fly:
    def __init__(self, pos, width, height, vector):
        self.pos = pos
        self.width = width
        self.height = height
        self.vector = vector
        self.endX = 1920
        self.speed = 10
        self.image = pygame.transform.scale(load_image(f'to_{self.vector}.png'), (width, height))

    def move(self, screen):

        if self.vector == 'right':
            if self.pos[0] < self.endX:
                self.pos[0] += (self.speed * random.random())
        else:
            if self.pos[0] > 0:
                self.pos[0] -= (self.speed * random.random())
        self.pos[1] -= self.speed

        screen.blit(self.image, self.pos)
