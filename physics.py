import math
from util import *

eps = 1e6
class Vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, tp):
        return Vector(tp[0], tp[1])
    

    def rotate(self, angle):
        angle = math.radians(angle)
        x2 = self.x * math.sin(angle) + self.y * math.cos(angle)
        y2 = self.x * math.cos(angle) - self.y * math.sin(angle)
        return Vector(x2, y2)

    def mod(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        return Vector(self.x / self.mod(), self.y / self.mod())
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
DEFAULT_SPEED = 1
RES_FORCE = 0.0025

class PhysicalBody:

    def __init__(self, x=0, y=0, vx=0, vy=0, ax=0, ay=0):
        self.pos = Vector(x, y)
        self.vel = Vector(vx, vy)
        self.a = Vector(ax, ay)
    
    def impulse(self, vec: Vector):
        self.vel += vec
        self.a = Vector(-RES_FORCE * self.vel.normalize().x, -RES_FORCE * self.vel.normalize().y)

    
    def update(self):
        if (isSameS(self.vel.x, self.a.x)):
            self.a.x = 0
            if (abs(self.vel.x) < eps): 
                self.vel.x = 0

        if (isSameS(self.vel.y, self.a.y)):
            self.a.y = 0
            if (abs(self.vel.y) < eps):
                self.vel.y = 0

        self.vel += self.a
        self.pos += self.vel