import pygame, sys, time, math
pygame.init()

swidth = 1080
sheight = 720
pwidth = 50
pheight = 50
screen = pygame.display.set_mode((swidth,sheight))
clock = pygame.time.Clock()

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((pwidth,pheight))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    # methods for player movement
    def moveH(self, mv):
        self.rect.x = mv
    def moveV(self, mv):
        self.rect.y = mv

players = pygame.sprite.Group()
player = PlayerSprite("red")
players.add(player)

player.rect.x = (swidth-pwidth)/2
player.rect.y = (sheight-pheight)/2
ppx = player.rect.x
ppy = player.rect.y

spd = 100

previousTime = time.time()

while True:
    # using deltatime for consistency
    dt = time.time() - previousTime
    previousTime = time.time()

    screen.fill((0,0,0))

    key = pygame.key.get_pressed()
    totKeys = sum(key)

    # account for diagonal speed: 1/sqrt(2) multiplier
    spdMultiplier = 1
    # conditions for diagonal keys
    if (((key[pygame.K_a] and key[pygame.K_w]) or 
         (key[pygame.K_a] and key[pygame.K_s]) or 
         (key[pygame.K_w] and key[pygame.K_d]) or 
         (key[pygame.K_s] and key[pygame.K_d])) and not
        # account for >2 direction inputs
        (key[pygame.K_a] and key[pygame.K_d] or 
         key[pygame.K_w] and key[pygame.K_s])
    ):
        spdMultiplier = 1/math.sqrt(2)
    else:
        # reset multiplier 
        spdMultiplier = 1

    players.update()
    # wasd directional movement
    if key[pygame.K_a] and ppx >= 150:
        ppx += -spd * dt * spdMultiplier
        player.moveH(ppx)
    if key[pygame.K_d] and ppx <= swidth-pwidth-150:
        ppx += spd * dt * spdMultiplier
        player.moveH(ppx)
    if key[pygame.K_w] and ppy >= 150:
        ppy += -spd * dt * spdMultiplier
        player.moveV(ppy)
    if key[pygame.K_s] and ppy <= sheight-pheight-150:
        ppy += spd * dt * spdMultiplier
        player.moveV(ppy)
    
    players.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

