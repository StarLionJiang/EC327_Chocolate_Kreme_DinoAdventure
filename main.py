import pygame, sys, time, math
from map import *
from assets import *

pygame.init()
clock = pygame.time.Clock()

# global speed value
spd = 250

previousTime = time.time()
state = 0

pygame.mouse.set_cursor(pygame.cursors.broken_x)

# check to see map; change tileScale
#TestMap()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    
    key = pygame.key.get_pressed()
    mClick = pygame.mouse.get_pressed()
    (mX,mY) = pygame.mouse.get_pos()
        
    if state == 0:
        screen.blit(title, titleRect)
        screen.blit(text, textRect)
        if key[pygame.K_SPACE]:
            state = 1

    elif state == 1:
        screen.blit(tutorial, tutorialRect)
        pygame.draw.rect(screen, (255,255,255), (800,416,160,160))
        screen.blit(cont, contRect)
        if mX > 800 and mX < 960 and mY > 416 and mY < 576 and mClick[0]:
            state = 2
        
    elif state == 2:
        # control var for previous location
        prePPX = ppx
        prePPY = ppy
        preMOX = mapOffsetX
        preMOY = mapOffsetY
                
        # deltatime for consistency
        dt = time.time() - previousTime
        previousTime = time.time()

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
        
        # screen edge and map border detenction and adjustments
        bigEdgeL = 0
        bigEdgeR = -mapWpx+swidth
        bigedgeU = 0
        bigedgeD = -mapHpx+sheight
        if mapOffsetX > bigEdgeL:
            mapEdge = True
            mapOffsetX = bigEdgeL
        if mapOffsetX < bigEdgeR:
            mapEdge = True
            mapOffsetX = bigEdgeR
        if mapOffsetY > bigedgeU:
            mapEdge = True
            mapOffsetY = bigedgeU
        if mapOffsetY < bigedgeD:
            mapEdge = True
            mapOffsetY = bigedgeD
            
        playerTileIndex[0] = round((ppx-mapOffsetX)/(tileDim*tileScale))
        playerTileIndex[1] = round((ppy-mapOffsetY)/(tileDim*tileScale))

        RenderLayer(mapOffsetX, mapOffsetY, mainMap)
        
        # check walking for animation cycling
        if not walking:
            walkingFrame = 2
            if playerFacingR:
                screen.blit(playerFrames[walkingFrame], (ppx, ppy-36))
            else:
                screen.blit(playerInvFrames[walkingFrame], (ppx, ppy-36))
        else:
            if playerFacingR:
                screen.blit(playerFrames[walkingFrame], (ppx, ppy-36))
            else:
                screen.blit(playerInvFrames[walkingFrame], (ppx, ppy-36))
            # cycling through sprites for walking animation
            walkingInterim += dt*spd/20
            walkingFrame = round(walkingInterim)
            if walkingFrame > 9:
                walkingFrame = 4
                walkingInterim = 4.0
                
        RenderLayer(mapOffsetX, mapOffsetY, overlay)
        
        # move to the left
        if key[pygame.K_a] and ppx >= mapBorder:
            playerFacingR = False
            ppx += -spd * dt * spdMultiplier
        elif (
            key[pygame.K_a] and ppx <= mapBorder and not 
            collisionMap[playerTileIndex[0]][playerTileIndex[1]]
        ):
            mapMove = True
            mapOffsetX += dt*spd * mapMove * spdMultiplier
            if ppx > 0 and mapOffsetX > 0:
                playerFacingR = False
                ppx += -spd * dt * spdMultiplier
        # move to the right
        mapBorderR = swidth-mapBorder-playerBaseDim*playerScale
        mapEdgePlayerR = mapBorderR + mapBorder
        if key[pygame.K_d] and ppx <= mapBorderR:
            playerFacingR = True
            ppx += spd * dt * spdMultiplier
        elif (
            key[pygame.K_d] and ppx >= mapBorderR and not 
            collisionMap[playerTileIndex[0]][playerTileIndex[1]]
        ):
            mapMove = True
            mapOffsetX += -dt*spd * mapMove * spdMultiplier
            if ppx < mapEdgePlayerR and mapOffsetX < bigEdgeR:
                playerFacingR = True
                ppx += spd * dt * spdMultiplier
        # move up
        if key[pygame.K_w] and ppy >= mapBorder:
            ppy += -spd * dt * spdMultiplier
        elif (
            key[pygame.K_w] and ppy <= mapBorder and not 
            collisionMap[playerTileIndex[0]][playerTileIndex[1]] 
        ):
            mapMove = True
            mapOffsetY += dt*spd * mapMove * spdMultiplier
            if ppy > 36 and mapOffsetY > 0:
                ppy += -spd * dt * spdMultiplier
        # move down
        mapBorderD = sheight-mapBorder-playerBaseDim*playerScale
        mapEdgePlayerD = mapBorderD + mapBorder
        if key[pygame.K_s] and ppy <= mapBorderD:
            ppy += spd * dt * spdMultiplier
        elif (
            key[pygame.K_s] and ppy >= mapBorderD and not 
            collisionMap[playerTileIndex[0]][playerTileIndex[1]]
        ):
            mapMove = True
            mapOffsetY += -dt*spd * mapMove * spdMultiplier
            if ppy < mapEdgePlayerD+36 and mapOffsetY < bigedgeD:
                ppy += spd * dt * spdMultiplier
        
        # check out of bound and reset positions
        pCenterX = ppx-mapOffsetX+playerBaseDim*playerScale/2
        pCenterY = ppy-mapOffsetY+playerBaseDim*playerScale/2
        if (# check L and R
            (collisionMap[playerTileIndex[0]-1][playerTileIndex[1]] and
            pCenterX < playerTileIndex[0]*tileDim*tileScale) or 
            (collisionMap[playerTileIndex[0]+1][playerTileIndex[1]] and
            pCenterX > playerTileIndex[0]*tileDim*tileScale+tileDim*tileScale)
        ):
            ppx = prePPX
            mapOffsetX = preMOX
        if (# check U and D
            (collisionMap[playerTileIndex[0]][playerTileIndex[1]-1] and
            pCenterY < playerTileIndex[1]*tileDim*tileScale) or 
            (collisionMap[playerTileIndex[0]][playerTileIndex[1]+1] and
            pCenterY > playerTileIndex[1]*tileDim*tileScale+tileDim*tileScale)
        ):
            ppy = prePPY
            mapOffsetY = preMOY
        
        mapMove = False
        mapEdge = False
        
    # cap FPS at 60
    clock.tick(60)

    pygame.display.update()
