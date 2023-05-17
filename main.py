import pygame
import random
from menu.menu import *

pygame.init()
pygame.font.init()

from ships import *

WIDTH = 1200
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for i in range(200)]

player1 = PlayerShip(keys1)
enemy = AI()

def play():
    global ismenu
    ismenu = False

# region menu
add_widget(Label(WIDTH / 2 - 250, 200, Text("S p a c e  S h o o t e r", pygame.font.Font("./images/font.woff", 40), (120, 10, 20))))
add_widget(Button(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), play, Text("Play", pygame.font.Font("./images/font.woff", 40), (0, 0, 0))))
# endregion

running = True
ismenu = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if ismenu:
        window.fill((88, 85, 79))

        draw_menu(window)
        update_menu(events)
        pygame.display.flip()
        continue
    
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
