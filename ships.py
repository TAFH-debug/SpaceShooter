from objects import *


class PlayerShip(Ship):

    def __init__(self, keys):
        super().__init__("images/playerShip.png")
        self.keys = keys
        self.shootcd = 100
        self.cdcounter = 0
        def offset(size):
            return Vector(-size.x / 2, 0)
        def offset2(size):
            return Vector(size.x / 2, 0)
        
        self.weapons = [Weapon(BulletType("images/laserBlue.png", 1000, 2, Vector(5, 29)), offset),
                        Weapon(BulletType("images/laserBlue.png", 1000, 2, Vector(5, 29)), offset2)]
        self.abilities = [Ability(pygame.K_g, 10000, 1000)]
        
        for i in self.abilities:
            object_manager.add_object(i)

    def update(self):
        super().update()
        
        set_x(self.center().x)
        set_y(self.center().y)

        pressed = pygame.key.get_pressed()
        
        for ability in self.abilities:
            ability.origin = (self.pos, self.size)
            ability.angle = self.angle
            if pressed[ability.key]:
                ability.use()
         
        if pygame.mouse.get_pressed()[0] and self.cdcounter >= self.shootcd:
            self.cdcounter = 0
            self.shoot(dn(Vector.from_tuple(pygame.mouse.get_pos())))
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
        norm = normalize(self.center())
        self.angle = angle(pos[0] - norm.x, -(pos[1] - norm.y)) - 90


class AI(Ship):

    def __init__(self):
        super().__init__("./images/enemyBlack1.png")