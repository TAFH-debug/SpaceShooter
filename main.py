import pygame
import random

pygame.init()
pygame.font.init()

from ships import *

WIDTH = 1200
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for i in range(200)]

player1 = PlayerShip(keys1)
enemy = AI()

running = True
while running:
    if True:
        draw_menu()
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
    
    pressed = pygame.key.get_pressed()
    # region logic
    object_manager.update()
    player1.update()
    enemy.update()
    # endregion

    # region draw
    window.fill((0, 0, 0))
    for i in stars:
        pygame.draw.circle(window, (255, 255, 255), i, 2)

    player1.draw(window)
    enemy.draw(window)
    object_manager.draw(window)
    pygame.display.flip()
    # endregion
