from core.objects import Team
from core.player import Vector
from .objects import *

class Core(GameObject, Destroyable):
    
    def __init__(self, data):
        GameObject.__init__(self, "./images/buildings/core.png", ObjectType.SHIP, Team.ENEMY)
        Destroyable.__init__(self, 1000)
        self.object_type = ObjectType.COLLIDEABLE
        self.pos = Vector(data['x'], data['y'])

    def draw(self, window):
        GameObject.draw(self, window)
        Destroyable.draw(self, window)

    def update(self):
        GameObject.update(self)
        Destroyable.update(self)

    def handle_collide(self, other):
        GameObject.handle_collide(self, other)
        if other.object_type == ObjectType.BULLET and self.team != other.team:
            self.health -= other.damage

