import pygame, sys, time, math, random
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

    RenderMap(mapOffsetX, mapOffsetY, ppx, ppy)

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

    if (
        key[pygame.K_w] or 
        key[pygame.K_a] or 
        key[pygame.K_s] or 
        key[pygame.K_d]
    ):
        walking = True
    else:
        walking = False

    # check walking for animation cycling
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
        # cycling through sprites for walking animation
        walkingInterim += dt*spd/20
        walkingFrame = round(walkingInterim)
        if walkingFrame > 9:
            walkingFrame = 4
            walkingInterim = 4

    #pygame.draw.rect(
    #    screen, (255,0,0), 
    #    (round(ppx+48), round(ppy+48), 4, 4)
    #)
    
    # screen edge and map border detenction and adjustments
    # screen shake when on map edge
    bigEdgeL = 0
    bigEdgeR = -tileDim*tileScale*len(mainMap)+swidth
    bigedgeU = 0
    bigedgeD = -tileDim*tileScale*len(mainMap[0])+sheight
    if mapOffsetX > bigEdgeL:
        mapEdge = True
        mapOffsetX = bigEdgeL + random.randint(-2,2)
    if mapOffsetX < bigEdgeR:
        mapEdge = True
        mapOffsetX = bigEdgeR + random.randint(-2,2)
    if mapOffsetY > bigedgeU:
        mapEdge = True
        mapOffsetY = bigedgeU + random.randint(-2,2)
    if mapOffsetY < bigedgeD:
        mapEdge = True
        mapOffsetY = bigedgeD + random.randint(-2,2)

    #print(noHit)
    # move to the left
    if (
        collisionMap[playerTileIndex[0]][playerTileIndex[1]] or
        collisionMap[playerTileIndex[0]-1][playerTileIndex[1]]
    ):
        if key[pygame.K_a] and ppx >= mapBorder:
            playerFacingR = False
            ppx += -spd * dt * spdMultiplier
        elif key[pygame.K_a] and ppx <= mapBorder:
            mapMove = True
            mapOffsetX += dt*spd * mapMove * spdMultiplier
            if ppx > 0 and mapOffsetX > 0:
                playerFacingR = False
                ppx += -spd * dt * spdMultiplier
    # move to the right
    mapBorderR = swidth-mapBorder-playerBaseDim*playerScale
    mapEdgePlayerR = mapBorderR + mapBorder
    if (
        collisionMap[playerTileIndex[0]][playerTileIndex[1]] or
        collisionMap[playerTileIndex[0]+1][playerTileIndex[1]]
    ):
        if key[pygame.K_d] and ppx <= mapBorderR:
            playerFacingR = True
            ppx += spd * dt * spdMultiplier
        elif key[pygame.K_d] and ppx >= mapBorderR:
            mapMove = True
            mapOffsetX += -dt*spd * mapMove * spdMultiplier
            if ppx < mapEdgePlayerR and mapOffsetX < bigEdgeR:
                playerFacingR = True
                ppx += spd * dt * spdMultiplier
    # move up
    if (
        collisionMap[playerTileIndex[0]][playerTileIndex[1]] or
        collisionMap[playerTileIndex[0]][playerTileIndex[1]-1]
    ):
        if key[pygame.K_w] and ppy >= mapBorder:
            ppy += -spd * dt * spdMultiplier
        elif key[pygame.K_w] and ppy <= mapBorder:
            mapMove = True
            mapOffsetY += dt*spd * mapMove * spdMultiplier
            if ppy > 0 and mapOffsetY > 0:
                ppy += -spd * dt * spdMultiplier
    # move down
    mapBorderD = sheight-mapBorder-playerBaseDim*playerScale
    mapEdgePlayerD = mapBorderD + mapBorder
    if (
        collisionMap[playerTileIndex[0]][playerTileIndex[1]] or
        collisionMap[playerTileIndex[0]][playerTileIndex[1]+1]
    ):
        if key[pygame.K_s] and ppy <= mapBorderD:
            ppy += spd * dt * spdMultiplier
        elif key[pygame.K_s] and ppy >= mapBorderD:
            mapMove = True
            mapOffsetY += -dt*spd * mapMove * spdMultiplier
            if ppy < mapEdgePlayerD and mapOffsetY < bigedgeD:
                ppy += spd * dt * spdMultiplier
    
    mapMove = False
    mapEdge = False
    
    # cap FPS at 60
    clock.tick(60)
    # print(clock.get_fps())

    pygame.display.update()
