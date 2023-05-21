import pygame
import random
from menu.menu import *
from scenes import *
from core.ui import *

pygame.init()
pygame.font.init()

from core.ships import *

WIDTH = 1200
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for i in range(200)]

pygame.mouse.set_visible(False)
cursor = Cursor("./images/cursor.png", Vector(20, 20))
player1 = PlayerShip(keys1)
ui = UI(player1)

object_manager.add_object(player1)
object_manager.add_object(ui)

scene = Scenes.MENU

lc = locals()
def st(nm, sc):
    lc[nm] = sc

# region menu
add_widget(Label(WIDTH / 2 - 250, 150, Text("S p a c e  S h o o t e r", pygame.font.Font("./images/font.woff", 40), (120, 10, 20))))
add_widget(Button(WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda: st("scene", Scenes.GAME)), Text("Play", pygame.font.Font("./images/font.woff", 40), (0, 0, 0))))
add_widget(Button(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda: st("scene", Scenes.INFO)), Text("Info", pygame.font.Font("./images/font.woff", 40), (0, 0, 0))))
add_widget(Button(WIDTH / 2 - 100, HEIGHT / 2 + 200, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda: st("running", False)), Text("Exit", pygame.font.Font("./images/font.woff", 40), (0, 0, 0))))
# endregion

running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if scene == Scenes.MENU:
        window.fill((78, 85, 79))

        draw_menu(window)
        update_menu(events)
    else:
        pressed = pygame.key.get_pressed()
        # region logic
        object_manager.update()
        # endregion

        # region draw
        window.fill((0, 0, 0))
        for i in stars:
            pygame.draw.circle(window, (255, 255, 255), i, 2)
        object_manager.draw(window)
        # endregion

    cursor.update()
    cursor.draw(window)

    pygame.display.flip()
