import pygame, sys, time, math
pygame.init()

swidth = 1080
sheight = 720
screen = pygame.display.set_mode((swidth,sheight))

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

playerSpriteW = 24
playerSpriteH = 24
# right facing player sprites
playerSpriteImg = pygame.image.load("doux.png").convert_alpha()
playerSpriteSheet = SpriteSheet(playerSpriteImg)

playerFrames = list()
for x in range(0,23):
    playerFrames.append(playerSpriteSheet.get_image(x, playerSpriteW, playerSpriteH, 3, (0,0,0)))

# left facing player sprites (inverted)
playerSpriteInv = pygame.transform.flip(playerSpriteImg, True, False)
playerSpriteInvSheet = SpriteSheet(playerSpriteInv)

playerInvFrames = list()
for x in range(23,-1,-1):
    playerInvFrames.append(playerSpriteInvSheet.get_image(x, playerSpriteW, playerSpriteH, 3, (0,0,0)))

# player location indices
ppx = swidth/2-playerSpriteW*2
ppy = sheight/2-playerSpriteH*2
pinitx = ppx
pinity = ppy
# walking animation control var
walkingFrame = 4
walkingInterim = walkingFrame
playerFacingR = True

# general speed value
spd = 200

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
    walking = False
    # conditions for diagonal keys
    if (
        ((key[pygame.K_a] and key[pygame.K_w]) or 
         (key[pygame.K_a] and key[pygame.K_s]) or 
         (key[pygame.K_w] and key[pygame.K_d]) or 
         (key[pygame.K_s] and key[pygame.K_d])
        ) and not
        # account for >2 direction inputs
        (key[pygame.K_a] and key[pygame.K_d] or 
         key[pygame.K_w] and key[pygame.K_s])
    ):
        spdMultiplier = 1/math.sqrt(2)
    else:
        # reset multiplier
        spdMultiplier = 1

    # check walking for animation cycling
    if (
        key[pygame.K_w] or 
        key[pygame.K_a] or 
        key[pygame.K_s] or 
        key[pygame.K_d]
    ):
        walking = True
    else:
        walking = False

    # cycling through sprites for walking animation
    if not walking:
        walkingFrame = 2
        if playerFacingR:
            screen.blit(playerFrames[walkingFrame], (ppx, ppy))
        else:
            screen.blit(playerInvFrames[walkingFrame], (ppx, ppy))
    else:
        if playerFacingR:
            screen.blit(playerFrames[walkingFrame], (ppx, ppy))
        else:
            screen.blit(playerInvFrames[walkingFrame], (ppx, ppy))
        walkingInterim += dt*spd/20
        walkingFrame = round(walkingInterim)
        if walkingFrame > 9:
            walkingFrame = 4
            walkingInterim = 4

    # wasd directional movement
    if key[pygame.K_a] and ppx >= 150:
        playerFacingR = False
        ppx += -spd * dt * spdMultiplier
    if key[pygame.K_d] and ppx <= swidth-playerSpriteW*2-150:
        playerFacingR = True
        ppx += spd * dt * spdMultiplier
    if key[pygame.K_w] and ppy >= 150:
        ppy += -spd * dt * spdMultiplier
    if key[pygame.K_s] and ppy <= sheight-playerSpriteH*2-150:
        ppy += spd * dt * spdMultiplier

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
