import pygame, sys, time, math
from map import *
from assets import *
pygame.init()
clock = pygame.time.Clock()

mapOffsetX = 0
mapOffsetY = 0
mapMove = False
mapEdge = False

# player location indices
ppx = swidth/2-playerBaseDim*2
ppy = sheight/2-playerBaseDim*2
pinitx = ppx
pinity = ppy
# walking animation control var
walkingFrame = 4
walkingInterim = walkingFrame
playerFacingR = True

# general speed value
spd = 250
previousTime = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # using deltatime for consistency
    dt = time.time() - previousTime
    previousTime = time.time()

    screen.fill((0,0,0))

    for x, i in enumerate(range(
        round(mapOffsetX),
        round(mapOffsetX)+len(mainMap)*tileDim*tileScale, 
        tileDim*tileScale
    )):
        for y, j in enumerate(range(
            round(mapOffsetY),
            round(mapOffsetY)+len(mainMap[0])*tileDim*tileScale, 
            tileDim*tileScale
        )):
            if (
                (i > -tileDim*tileScale and i < swidth) and
                (j > -tileDim*tileScale and j < sheight)
            ):
                screen.blit(tileList[mainMap[x][y]], (i,j))

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
    if key[pygame.K_a] and ppx >= mapBorder:
        playerFacingR = False
        ppx += -spd * dt * spdMultiplier
    elif key[pygame.K_a] and ppx <= mapBorder:
        mapMove = True
        mapOffsetX += dt*spd * mapMove
    if key[pygame.K_d] and ppx <= swidth-mapBorder-playerBaseDim*playerScale:
        playerFacingR = True
        ppx += spd * dt * spdMultiplier
    elif key[pygame.K_d] and ppx >= swidth-mapBorder-playerBaseDim*playerScale:
        mapMove = True
        mapOffsetX += -dt*spd * mapMove
    if key[pygame.K_w] and ppy >= mapBorder:
        ppy += -spd * dt * spdMultiplier
    elif key[pygame.K_w] and ppy <= mapBorder:
        mapMove = True
        mapOffsetY += dt*spd * mapMove
    if key[pygame.K_s] and ppy <= sheight-mapBorder-playerBaseDim*playerScale:
        ppy += spd * dt * spdMultiplier
    elif key[pygame.K_s] and ppy >= sheight-mapBorder-playerBaseDim*playerScale:
        mapMove = True
        mapOffsetY += -dt*spd * mapMove
    
    mapMove = False

    pygame.display.update()
