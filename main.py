import pygame

pygame.init()
pygame.font.init()

from objects import *
from player import *
from ships import *

WIDTH = 1200
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

player1 = PlayerShip(keys1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
    
    pressed = pygame.key.get_pressed()
    #region logic
    object_manager.update()
    player1.update()
    #endregion

    #region draw
    window.fill((0, 0, 0))
    player1.draw(window)
    object_manager.draw(window)
    pygame.display.flip()
    #endregion