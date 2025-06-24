import pygame, math

pygame.init()
W, H = 600, 400
win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock() #framerate

# Colors
RED, GREEN, BLUE = (255,0,0), (0,255,0), (0,0,255)

# Bloon class, (can be broken up into seperate files)
class Bloon:
    def __init__(self):
        self.x, self.y = 0, 200
        self.speed = 2
    def move(self):
        self.x += self.speed
    def draw(self): #render on screen
        pygame.draw.circle(win, RED, (int(self.x), self.y), 10) #where its appearing,just circles, red, tuple, size

# Tower class
class Tower:
    def __init__(self):
        self.x, self.y = 300, 200
        self.range = 100
        self.cooldown = 30
        self.timer = 0
    def draw(self):
        pygame.draw.circle(win, BLUE, (self.x, self.y), 10) #appears in screen, color blue, where its appearing (position), size
    def can_shoot(self, bloon):
        dist = math.hypot(bloon.x - self.x, bloon.y - self.y)
        return dist < self.range and self.timer <= 0

# Projectile class
class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        self.tx, self.ty = target.x, target.y #target position
        dx, dy = self.tx - x, self.ty - y
        dist = math.hypot(dx, dy)
        self.vx, self.vy = dx / dist * 5, dy / dist * 5
    def move(self):
        self.x += self.vx
        self.y += self.vy
    def draw(self):
        pygame.draw.circle(win, GREEN, (int(self.x), int(self.y)), 5)
    def hit(self, bloon):
        return math.hypot(self.x - bloon.x, self.y - bloon.y) < 10 # just an estimation

# Game objects
bloon = Bloon() #how you create the objects
tower = Tower()
bullets = [] #append or add bullets later

# Main loop
run = True
while run:
    clock.tick(60) #60 fps
    win.fill((255,255,255)) #color background (white)

    bloon.move()
    bloon.draw()

    tower.draw()
    if tower.can_shoot(bloon):
        bullets.append(Bullet(tower.x, tower.y, bloon))
        tower.timer = tower.cooldown
    tower.timer -= 1

    for b in bullets[:]: # the [:] means from 0 to the last one or [100:](?) from 100 to the last 
        b.move()
        b.draw()
        if b.hit(bloon):
            bullets.remove(b) #removes a specific bullet that hits
            bloon.x = 0  # Reset bloon, its just pushing the balloom back, definitely not what btd6 does

    pygame.display.flip() #pygame.display.update() works like flip, updates changes

    for e in pygame.event.get(): #bascally event, every event iin keyboard & mouse
        if e.type == pygame.QUIT: #checking if they want to quit, x button
            run = False

pygame.quit()
