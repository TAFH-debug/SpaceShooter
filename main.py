import pygame
from objects import *

pygame.init()

window = pygame.display.set_mode((1200, 800))

keys1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "left": pygame.K_a,
    "debug": pygame.K_f
}

player1 = Player(keys1)

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