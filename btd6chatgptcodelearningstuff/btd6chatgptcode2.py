import pygame, math

pygame.init()
W, H = 600, 400
win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Load bloon image
bloon_img = pygame.image.load("balloon.png")
bloon_img = pygame.transform.scale(bloon_img, (30, 40))  # Resize if needed

playerpic = pygame.image.load("characters/player.png")
playerpic = pygame.transform.scale(playerpic, (40,40))

# Colors
GREEN, BLUE = (0,255,0), (0,0,255)

# Bloon class
class Bloon:
    def __init__(self):
        self.x, self.y = 0, 200
        self.speed = 2
    def move(self):
        self.x += self.speed
    def draw(self):
        win.blit(bloon_img, (int(self.x), self.y - 20))  # Center the image, win.blit displays the image on win, the image, location, location

# Tower class
class Tower:
    def __init__(self):
        self.x, self.y = 300, 200
        self.range = 100
        self.cooldown = 30
        self.timer = 0
    def draw(self):
        win.blit(playerpic, (self.x, self.y -20)) #int probably not needed, added -20 to fix offset
    def can_shoot(self, bloon):
        return math.hypot(bloon.x - self.x, bloon.y - self.y) < self.range and self.timer <= 0

# Bullet class
class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        dx, dy = target.x - x, target.y - y
        dist = math.hypot(dx, dy)
        self.vx, self.vy = dx / dist * 5, dy / dist * 5
    def move(self):
        self.x += self.vx
        self.y += self.vy
    def draw(self):
        pygame.draw.circle(win, GREEN, (int(self.x), int(self.y)), 5)
    def hit(self, bloon):
        return math.hypot(self.x - bloon.x, self.y - bloon.y) < 20

# Game objects
bloon = Bloon()
tower = Tower()
bullets = []

# Main loop
run = True
while run:
    clock.tick(60)
    win.fill((255,255,255))

    bloon.move()
    bloon.draw()

    tower.draw()
    if tower.can_shoot(bloon):
        bullets.append(Bullet(tower.x, tower.y, bloon))
        tower.timer = tower.cooldown
    tower.timer -= 1

    for b in bullets[:]:
        b.move()
        b.draw()
        if b.hit(bloon):
            bullets.remove(b)
            bloon.x = 0  # Reset position

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

pygame.quit()
