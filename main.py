import pygame, sys, time, math
from map import *
from assets import *

pygame.init()
clock = pygame.time.Clock()

# global speed value
spd = 250
previousTime = time.time()

# check to see map; change tileScale
#TestMap()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # deltatime for consistency
    dt = time.time() - previousTime
    previousTime = time.time()

    screen.fill((0,0,0))

    RenderMap(mapOffsetX, mapOffsetY)

    key = pygame.key.get_pressed()
    totKeys = sum(key)

    # account for diagonal speed: 1/sqrt(2) multiplier
    spdMultiplier = 1
    walking = False
    if (
        ((key[pygame.K_a] and key[pygame.K_w]) or 
         (key[pygame.K_a] and key[pygame.K_s]) or 
         (key[pygame.K_w] and key[pygame.K_d]) or 
         (key[pygame.K_s] and key[pygame.K_d])
        ) and not
        ((key[pygame.K_a] and key[pygame.K_d]) or 
         (key[pygame.K_w] and key[pygame.K_s]))
    ):
        spdMultiplier = 1/math.sqrt(2)
    else:
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
        # walking frame iteration
        walkingInterim += dt*spd/20
        walkingFrame = round(walkingInterim)
        if walkingFrame > 9:
            walkingFrame = 4
            walkingInterim = 4

    # screen edge and map border detenction and adjustments
    bigEdgeL = 0; bigedgeU = 0
    bigEdgeR = -tileDim*tileScale*len(mainMap)+swidth
    bigEdgeB = -tileDim*tileScale*len(mainMap[0])+sheight
    if mapOffsetX > bigEdgeL:
        mapEdge = True
        mapOffsetX = bigEdgeL
    if mapOffsetX < bigEdgeR:
        mapEdge = True
        mapOffsetX = bigEdgeR
    if mapOffsetY > bigedgeU:
        mapEdge = True
        mapOffsetY = bigedgeU
    if mapOffsetY < bigEdgeB:
        mapEdge = True
        mapOffsetY = bigEdgeB

    # move to the left
    if key[pygame.K_a] and ppx >= mapBorder:
        playerFacingR = False
        ppx += -spd * dt * spdMultiplier
    elif key[pygame.K_a] and ppx <= mapBorder:
        mapMove = True
        mapOffsetX += dt*spd * mapMove
        if ppx > 0 and mapOffsetX > 0:
            playerFacingR = False
            ppx += -spd * dt * spdMultiplier
    # move to the right
    mapBorderR = swidth-mapBorder-playerBaseDim*playerScale
    mapEdgePlayerR = mapBorderR + mapBorder
    if key[pygame.K_d] and ppx <= mapBorderR:
        playerFacingR = True
        ppx += spd * dt * spdMultiplier
    elif key[pygame.K_d] and ppx >= mapBorderR:
        mapMove = True
        mapOffsetX += -dt*spd * mapMove
        if ppx < mapEdgePlayerR and mapOffsetX < bigEdgeR:
            playerFacingR = True
            ppx += spd * dt * spdMultiplier
    # move up
    if key[pygame.K_w] and ppy >= mapBorder:
        ppy += -spd * dt * spdMultiplier
    elif key[pygame.K_w] and ppy <= mapBorder:
        mapMove = True
        mapOffsetY += dt*spd * mapMove
        if ppy > 0 and mapOffsetY > 0:
            ppy += -spd * dt * spdMultiplier
    # move down
    mapBorderD = sheight-mapBorder-playerBaseDim*playerScale
    mapEdgePlayerD = mapBorderD + mapBorder
    if key[pygame.K_s] and ppy <= mapBorderD:
        ppy += spd * dt * spdMultiplier
    elif key[pygame.K_s] and ppy >= mapBorderD:
        mapMove = True
        mapOffsetY += -dt*spd * mapMove
        if ppy < mapEdgePlayerD and mapOffsetY < bigEdgeB:
            ppy += spd * dt * spdMultiplier
    
    mapMove = False
    mapEdge = False

    clock.tick()
    #print(clock.get_fps())

    pygame.display.update()
