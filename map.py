import pygame, sys
from assets import *
pygame.init()

# start screen text
textFont = pygame.font.Font("freesansbold.ttf", 24)
text = textFont.render("--- press space to start ---", True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.center = (swidth//2, sheight//2+150)
titleFont = pygame.font.Font("freesansbold.ttf", 64)
title = titleFont.render("Dino Adventure", True, (255,255,255), (0,0,0))
titleRect = title.get_rect()
titleRect.center = (swidth//2, sheight//2)

# transpose map matrix for compatibility

mapBorder = 150
mapOffsetX = 0
mapOffsetY = 0
mapMove = False
mapEdge = False

def transpose(l1, l2):
    for i in range(len(l1[0])):
        # print(i)
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2

# map matrix with asset value at each tile location
mainMapOg = [[ 2,42, 2, 0, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0], 
             [39,40,40,39, 2, 1, 0, 2, 2, 0, 0, 1, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0], 
             [40, 1, 2,40,42, 2, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 2, 1, 0, 0, 1, 1], 
             [42, 2, 2, 2,41, 0,39, 2, 0,42, 0, 1, 2, 2,40, 2, 0, 1, 2, 0, 1, 0], 
             [ 0, 0, 0,41,39,42,40,40,42,39,41, 0, 0, 0,39,40,39,41,41,42,40,41], 
             [ 0, 2, 1, 0, 0,41, 0, 1, 2, 2,39, 0,41, 1,42, 0, 1, 1, 2, 2, 2, 0], 
             [ 0, 0, 1,41, 0,39, 1, 0, 1, 1,42,39,42,39,41, 1, 2, 0, 1, 1, 1, 0], 
             [ 2, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0, 2, 1,40, 0, 2, 1, 2, 1, 2, 0, 2], 
             [ 1, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0,42,39,41, 0, 2, 1, 2, 2, 1, 2, 2], 
             [ 1, 1, 2, 0, 0, 2, 1, 0, 0, 1, 1,42, 1, 2, 0, 0, 2, 0, 0, 0, 1, 1], 
             [ 1, 2, 2, 2, 2, 0, 1, 2, 0, 1, 0,39, 2, 1, 2, 2, 2, 0, 2, 2, 1, 2], 
             [ 0, 0, 0, 1, 2, 0, 1, 2, 2, 2, 0,40, 0, 0, 1, 1, 1, 0, 1, 2, 2, 0], 
             [ 0, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0,41, 0, 2, 1, 2, 0, 2, 1, 0, 0, 1], 
             [ 0, 0, 1, 2, 1, 2, 2, 1, 2, 0, 2,42, 2, 2, 2, 0, 0, 1, 1, 2, 2, 2]]

# transpose for RenderMap to read into for loops
mainMap = []
mainMap = transpose(mainMapOg, mainMap)

collisionMapOg = [[1]*(len(mainMap)+1)]*(len(mainMap[0])+1)

collisionMap = []
collisionMap = transpose(collisionMapOg, collisionMap)

overlayOg = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], 
             [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]

overlay = []
overlay = transpose(overlayOg, overlay)

for i in range(len(mainMap)):
    for j in range(len(mainMap[0])):
        if mainMap[i][j] in range(39,43):
            collisionMap[i][j] = 0

# map preview frunction

mapWpx = len(mainMap)*tileDim*tileScale
mapHpx = len(mainMap[0])*tileDim*tileScale

playerTileIndex = [0,0]

def RenderLayer(mapOX, mapOY, grid):
    for x, i in enumerate(range(
        round(mapOX),
        round(mapOX)+mapWpx, 
        tileDim*tileScale
    )):
        for y, j in enumerate(range(
            round(mapOY),
            round(mapOY)+mapHpx, 
            tileDim*tileScale
        )):
            # only render tiles within the game window
            if (
                (i > -tileDim*tileScale and i < swidth) and
                (j > -tileDim*tileScale and j < sheight) and
                grid[x][y] != -1
            ):
                screen.blit(tileList[grid[x][y]], (i,j))
    
def TestMap():
    centeringX = int((swidth-mapWpx)/2)
    centeringY = int((sheight-mapHpx)/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))

        for x, i in enumerate(range(
            centeringX, 
            centeringX+mapWpx, 
            tileDim*tileScale
        )):
            for y, j in enumerate(range(
                centeringY, 
                centeringY+mapHpx, 
                tileDim*tileScale
            )):
                screen.blit(tileList[mainMap[x][y]], (i,j))

        pygame.display.update()
