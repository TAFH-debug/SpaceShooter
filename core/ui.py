import pygame
from .objects import *


class Cursor:

    def __init__(self, path, size):
        self.sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size.to_tuple())
        self.size = size

    def update(self):
        self.pos = Vector.from_tuple(pygame.mouse.get_pos())

    def draw(self, window):
        rect = self.sprite.get_rect()
        rect.x = self.pos.x
        rect.y = self.pos.y
        if DEBUG:
            pygame.draw.rect(window, (0, 255, 0), rect, 1)
        window.blit(self.sprite, rect)


class UI:

    def __init__(self, player):
        self.player = player

    def draw(self, window):
        n = 1 - self.player.weapons[0].cooldown.counter / self.player.weapons[0].cooldown.initial
        pygame.draw.rect(window, (0, 25, 150), (75, 675, 75, 75))
        pygame.draw.rect(window, (0, 50, 200), (75, 675 + n * 75, 75, 75 - n * 75))

        x = 1 - self.player.abilities[0].cooldown.counter / self.player.abilities[0].cooldown.initial
        pygame.draw.rect(window, (150, 25, 0), (75, 575, 75, 75))
        pygame.draw.rect(window, (200, 50, 0), (75, 575 + x * 75, 75, 75 - x * 75))

    def update(self):
        pass