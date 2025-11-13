import pygame


class Bird(object):
    def __init__(self, x, y, width, height, assets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.assets = assets
        self.vel = 1.4
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(self.assets.bird, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False


class Saw(object):
    def __init__(self, x, y, width, height, assets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.assets = assets
        self.rotateCount = 0
        self.vel = 1.4
        self.hitbox = (self.x + 10, self.y + 5,
                       self.width - 20, self.height - 5)

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5,
                       self.width - 20, self.height - 5)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(
            self.assets.saw_rotate[self.rotateCount // 2], (64, 64)), (self.x, self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class Spike(Saw):
    def __init__(self, x, y, width, height, assets):
        super().__init__(x, y, width, height, assets)
        self.hitbox = (self.x + 10, self.y, 28, 315)

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.assets.spike_img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


class GroundEnemy(object):
    def __init__(self, x, y, width, height, assets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.assets = assets
        self.vel = 1.4
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(self.assets.ground_enemy, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False
