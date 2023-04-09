import pygame
import object_manager
from physics import *

DEBUG = False

class Object:

    def __init__(self, path, size: Vector=None):
        if not (size == None):
            self.sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size.to_tuple())
            self.size = size
        else:
            self.sprite = pygame.image.load(path).convert_alpha()
            self.size = Vector.from_tuple(self.sprite.get_size())
        self.angle = 0
        
    def draw(self, window):
        rs, rect = rot_center(self.sprite, self.angle, self.center())
        if DEBUG:
            pygame.draw.rect(window, (0, 255, 0), rect, 1)
        window.blit(rs, rect)
    
    def update(self):
        pass

    def center(self):
        return self.pos + Vector(self.size.x / 2, self.size.y / 2)

class BulletType:

    def __init__(self, path, lifetime, speed, size=None):
        self.path = path
        self.speed = speed
        self.lifetime = lifetime
        self.size = size

    def create_instance(self, origin, angle):
        bullet = Bullet(self.path, self.lifetime, self.speed, self, origin.x, origin.y, angle, self.size)
        object_manager.add_object(bullet)

class Bullet(Object, PhysicalBody):

    def __init__(self, path, lifetime, speed, btype, x, y, angle, size=None):
        Object.__init__(self, path, size)
        PhysicalBody.__init__(self, x, y)
        self.lifetime = lifetime
        self.speed = speed
        self.btype = btype
        self.angle = angle
        self.vel = Vector(-self.speed, 0).rotate(self.angle)

    def update(self):
        if not pygame.display.get_surface().get_rect().collidepoint(self.pos.to_tuple()):
            object_manager.remove_object(self)
            return
        self.pos += self.vel

class Weapon:

    def __init__(self, bullet_type, offset_calc):
        self.bullet_type = bullet_type
        self.offset_calc = offset_calc

    def shoot(self, target: Vector, origin: Vector, angle):
        self.bullet_type.create_instance(origin, angle)


class Ship(PhysicalBody, Object):
    
    def __init__(self, path, weapons: list[Weapon]=[], size=None):
        PhysicalBody.__init__(self)
        Object.__init__(self, path, size)
        self.weapons = weapons
        self.coords = []

        self.gcounter = 0
        
    def shoot(self, target):
        for weapon in self.weapons:
            offset = weapon.offset_calc(self.size).rotate(self.angle + 90)
            weapon.shoot(target, offset + self.center(), self.angle)

    def update(self):
        PhysicalBody.update(self)

        if len(self.coords) == 0 or (self.pos.x != self.coords[-1].x or self.pos.y != self.coords[-1].y):
            self.coords.append(self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2))
            if len(self.coords) > 100:
                self.coords.pop(0)

    def draw(self, window):
        pygame.draw.circle(window, (255, 75, 0), 
                           (self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2)).to_tuple(),
                           abs(5 * math.sin(self.gcounter / 100)) + 10)
        pygame.draw.circle(window, (255, 125, 0), 
                           (self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2)).to_tuple(),
                           5)
        
        self.gcounter += 1

        
        idx = 0
        for i in self.coords:
            idx += 1
            pygame.draw.circle(window, (255, 0, 0), i.to_tuple(), 7.5 * idx / 100)
            
        super().draw(window)

class Player(Ship):

    def __init__(self, keys):
        super().__init__("images/playerShip.png")
        self.keys = keys
        self.shootcd = 100
        self.cdcounter = 0
        def offset(size):
            return Vector(-size.x / 2, 0)
        def offset2(size):
            return Vector(size.x / 2, 0)
        self.weapons = [Weapon(BulletType("images/laserBlue.png", 1, 1, Vector(5, 29)), offset),
                        Weapon(BulletType("images/laserBlue.png", 1, 1, Vector(5, 29)), offset2)]
    
    def update(self):
        super().update()

        pressed = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] and self.cdcounter >= self.shootcd:
            self.cdcounter = 0
            self.shoot(pygame.mouse.get_pos())
        else:
            self.cdcounter += 1
        if pressed[self.keys['up']] and self.vel.y > -0.5:
            self.impulse(Vector(0, -DEFAULT_SPEED))
        if pressed[self.keys['down']] and self.vel.y < 0.5:
            self.impulse(Vector(0, DEFAULT_SPEED))
        if pressed[self.keys['right']] and self.vel.x < 0.5:
            self.impulse(Vector(DEFAULT_SPEED, 0))
        if pressed[self.keys['left']] and self.vel.x > -0.5:
            self.impulse(Vector(-DEFAULT_SPEED, 0))
        if pressed[self.keys['debug']]:
            pass

        pos = pygame.mouse.get_pos()
        self.angle = angle(pos[0] - self.center().x, -(pos[1] - self.center().y)) - 90
