import json
from .physics import *
from .ships import *
from .buildings import *


class Level:

    def __init__(self, path):
        self.path = path

    def load(self):
        
        with open(self.path, "r") as file:
            data = json.load(file)
            core = data['core']
            enemies = data['enemies']

        self.core = Core(core)
        object_manager.add_object(self.core)
        for i in enemies:
            enemy = AI()
            enemy.pos = Vector(i['x'], i['y'])
            object_manager.add_object(enemy)

    def step(self, window):
        if self.core.health <= 0:
            return True   

        pos = self.core.pos - get()
        ang = angle(pos.x, -pos.y)
        pygame.draw.circle(window, (175, 55, 80), (normalize(get()) + Vector(0, 50).rotate(ang)).to_tuple(), 20)
        
        return False

