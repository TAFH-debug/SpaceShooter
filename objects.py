import pygame
import object_manager
from physics import *
from player import *

DEBUG = False

class Object:

    def __init__(self, path, size: Vector=None):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        if not (size == None):
            self.sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size.to_tuple())
            self.size = size
        else:
            self.sprite = pygame.image.load(path).convert_alpha()
            self.size = Vector.from_tuple(self.sprite.get_size())
        self.angle = 0
        
    def draw(self, window):
        rs, rect = rot_center(self.sprite, self.angle, self.center())
        nzed = normalize(Vector(rect.x, rect.y))
        rect.x = nzed.x
        rect.y = nzed.y
        if DEBUG:
            window.blit(self.font.render(str(rect.x) + " " + str(rect.y), False, (255, 0, 0)), (0, 0))
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
        if self.lifetime < 0:
            object_manager.remove_object(self)
            return
        self.lifetime -= 1
        self.pos += self.vel

class Ability:
    
    def __init__(self, key, cooldown: int, use_time: int):
        self.key = key
        self.cooldown = Counter(cooldown, False)
        self.use_time = Counter(use_time)
        self.using = False
        self.origin = Vector(0, 0), Vector(0, 0)
        self.angle = 0
    
    def use(self):
        if not self.cooldown.done():
            return
        self.using = True
        
    def update(self):
        if self.use_time.done():
            self.using = False
        elif self.using == True:
            self.use_time.step()
        self.cooldown.step()
    
    def draw(self, window):
        if self.using:
            center_offset = Vector(self.origin[1].x / 2, self.origin[1].y / 2) + self.origin[0]
            start_pos = normalize((Vector(0, -self.origin[1].y / 2).rotate(self.angle - 90) + center_offset)).to_tuple()
            end_pos = normalize((Vector(0, -(self.origin[1].y / 2 + 200)).rotate(self.angle - 90) + center_offset)).to_tuple()
            pygame.draw.line(window, (255, 0, 0),
                             start_pos,
                             end_pos,
                             int(5 * math.sin(self.use_time.counter / 100) + 25))
            pygame.draw.line(window, (255, 125, 0),
                             start_pos,
                             end_pos,
                             10)
            pygame.draw.circle(window, (255, 0, 0), end_pos, int(5 * math.sin(self.use_time.counter / 100) + 25) / 2)

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
        cpos = normalize((self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2))).to_tuple()
        pygame.draw.circle(window, (255, 75, 0), cpos, abs(5 * math.sin(self.gcounter / 100)) + 10)
        pygame.draw.circle(window, (255, 125, 0), cpos, 5)
        
        self.gcounter += 1
        
        
        idx = 0
        for i in self.coords:
            idx += 1
            pygame.draw.circle(window, (255, 0, 0), normalize(i).to_tuple(), 7.5 * idx / 100)
            
        super().draw(window)
