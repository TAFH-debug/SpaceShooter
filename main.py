import pygame
import random
from core.level_loader import *
from menu import menu
from menu.widgets import *
from scenes import *
from core.ui import *
from os import listdir
from os.path import isfile, join

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

ll = None

scene = Scenes.MENU

lc = locals()
def st(nm, sc):
    lc[nm] = sc

# region menu
menu.add_menu('menu')
menu.add_widget('menu', Label(WIDTH / 2 - 250, 150, Text("S p a c e  S h o o t e r", pygame.font.Font("./images/font.woff", 40), (120, 10, 20))))
menu.add_widget('menu', Button(WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda _: st("scene", Scenes.LEVELS)), Text("Play", pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0))))
menu.add_widget('menu', Button(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda _: st("scene", Scenes.INFO)), Text("Info", pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0))))
menu.add_widget('menu', Button(WIDTH / 2 - 100, HEIGHT / 2 + 200, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda _: st("running", False)), Text("Exit", pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0))))
# endregion

# region info
menu.add_menu('info')
menu.add_widget('info', Label(WIDTH / 2 - 250, 150, Text("S p a c e  S h o o t e r", pygame.font.Font("./images/font.woff", 40), (120, 10, 20))))
menu.add_widget('info', Label(WIDTH / 2 - 350, 300, Text("W A S D - Перемещение вверх, вниз, вправо, налево.", pygame.font.SysFont("Arial", 30), (120, 10, 20))))
menu.add_widget('info', Label(WIDTH / 2 - 350, 350, Text("Левая кнопка мыши (ЛКМ) - Стрельба", pygame.font.SysFont("Arial", 30), (120, 10, 20))))
menu.add_widget('info', Label(WIDTH / 2 - 350, 400, Text("G - Способность", pygame.font.SysFont("Arial", 30), (120, 10, 20))))
menu.add_widget('info', Button(WIDTH / 2 - 100, HEIGHT / 2 + 200, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda _: st("scene", Scenes.MENU)), Text("Return", pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0))))
# endregion

# region levels
menu.add_menu('lvls')
menu.add_widget('lvls', Label(WIDTH / 2 - 250, 150, Text("S p a c e  S h o o t e r", pygame.font.Font("./images/font.woff", 40), (120, 10, 20))))

levels = [join("./levels", f) for f in listdir("./levels")]
idx = 1
for j in levels:
    def g(nm):
        global scene
        global ll
        scene = Scenes.GAME
        ll = Level(nm)
        ll.load()
    menu.add_widget('lvls', Button(300 + (idx - 1) * 300, HEIGHT / 2, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), lambda x: g(x), Text(str(idx), pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0)), j))
    idx += 1
menu.add_widget('lvls', Button(WIDTH / 2 - 100, HEIGHT / 2 + 200, 200, 100, Clicked((125, 126, 0), Border(2, (50, 40, 45), 10)),
                  (144, 155, 0), Border(2, (50, 40, 45), 10), (lambda _: st("scene", Scenes.MENU)), Text("Return", pygame.font.Font("./images/kvf.ttf", 40), (0, 0, 0))))
# endregion

running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))

    if scene == Scenes.MENU:
        window.fill((78, 85, 79))

        menu.draw_menu(window, 'menu')
        menu.update_menu(events, 'menu')
    elif scene == Scenes.GAME:
        pressed = pygame.key.get_pressed()
        # region logic
        object_manager.update()
        if ll.step(window):
            scene = Scenes.MENU
            object_manager.clear()
            player1 = PlayerShip(keys1)
            ui.player = player1
            object_manager.add_object(ui)
            object_manager.add_object(player1)
        # endregion

        # region draw
        for i in stars:
            pygame.draw.circle(window, (255, 255, 255), i, 2)
        object_manager.draw(window)
        # endregion
    elif scene == Scenes.INFO:
        window.fill((78, 85, 79))

        menu.draw_menu(window, 'info')
        menu.update_menu(events, 'info')
    elif scene == Scenes.LEVELS:
        window.fill((78, 85, 79))

        menu.draw_menu(window, 'lvls')
        menu.update_menu(events, 'lvls')
    
    
    cursor.update()
    cursor.draw(window)

    pygame.display.flip()
