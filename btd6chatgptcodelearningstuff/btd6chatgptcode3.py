import pygame, math, random

pygame.init()
W, H = 800, 600
win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Load and scale balloon image
balloon_img = pygame.image.load("balloon.png")
balloon_img = pygame.transform.scale(balloon_img, (30, 40))

# Colors
GREEN, BLUE = (0,255,0), (0,0,255)

# Path (x, y coordinates)
path = [(0, 300), (200, 300), (200, 500), (600, 500), (600, 100), (800, 100)] #hits a wall and makes a turn (a guess)

# Bloon class with path following
class Bloon:
    def __init__(self):
        self.x, self.y = path[0]
        self.path_index = 0
        self.speed = 2
    def move(self):
        if self.path_index + 1 < len(path):
            target = path[self.path_index + 1]
            dx, dy = target[0] - self.x, target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist < 1:
                self.path_index += 1
            else:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
    def draw(self):
        win.blit(balloon_img, (int(self.x) - 15, int(self.y) - 20))

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 120
        self.cooldown = 30
        self.timer = 0
    def draw(self):
        pygame.draw.circle(win, BLUE, (self.x, self.y), 10)
    def can_shoot(self, bloon):
        return math.hypot(bloon.x - self.x, bloon.y - self.y) < self.range and self.timer <= 0

# Bullet class
class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        self.target = target
        dx, dy = target.x - x, target.y - y
        dist = math.hypot(dx, dy)
        self.vx, self.vy = dx / dist * 5, dy / dist * 5
    def move(self):
        self.x += self.vx
        self.y += self.vy
    def draw(self):
        pygame.draw.circle(win, GREEN, (int(self.x), int(self.y)), 5)
    def hit(self):
        return math.hypot(self.x - self.target.x, self.y - self.target.y) < 20

# Game objects
bloons = [] #now an array
bullets = []
towers = [Tower(250, 250), Tower(550, 300)] #also an array, preset to have 2 towers
spawn_timer = 0

# Main loop
run = True
while run:
    clock.tick(60)
    win.fill((255,255,255))

    # Spawn bloons every 60 frames (~1 second)
    spawn_timer += 2.5 # how many ballons spawn in 60 secs (1= 1 every 60s)
    if spawn_timer >= 60:
        bloons.append(Bloon())
        spawn_timer = 0

    # Move & draw bloons
    for b in bloons[:]:
        b.move()
        b.draw()
        if b.path_index >= len(path) - 1:
            bloons.remove(b)  # Bloon reached the end

    # Towers shoot
    for tower in towers:
        tower.draw()
        for b in bloons:
            if tower.can_shoot(b):
                bullets.append(Bullet(tower.x, tower.y, b))
                tower.timer = tower.cooldown
                break
        tower.timer -= 1

    # Move & draw bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        if bullet.hit():
            if bullet.target in bloons:
                bloons.remove(bullet.target)
            bullets.remove(bullet)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

pygame.quit()
