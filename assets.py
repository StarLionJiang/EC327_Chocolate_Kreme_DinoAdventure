import pygame, os
import spriteSheet
swidth = 960
sheight = 576
screen = pygame.display.set_mode((swidth,sheight))

playerBaseDim = 24
playerScale = 4

# right facing player sprites
playerSpriteImg = pygame.image.load("doux.png").convert_alpha()
playerSpriteSheet = spriteSheet.SpriteSheet(playerSpriteImg)

playerFrames = []
for x in range(0,23):
    playerFrames.append(
        playerSpriteSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# left facing player sprites (inverted)
playerSpriteInv = pygame.transform.flip(playerSpriteImg, True, False)
playerSpriteInvSheet = spriteSheet.SpriteSheet(playerSpriteInv)

playerInvFrames = []
for x in range(23,-1,-1):
    playerInvFrames.append(
        playerSpriteInvSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# tile square assets for map
tileScale = 1#int((3/2)*playerScale)
tileDim = 16
tileSprites = []
path = "C:/Users/alvin/Desktop/PyGame/PyGame-First/MapAssets/Tiles"
dirlist = os.listdir(path)
for x in range(len(dirlist)):
    tileSprites.append(pygame.image.load(f"MapAssets/Tiles/{dirlist[x]}"))

tileList = []
for x in range(len(tileSprites)):
    tileList.append(spriteSheet.SpriteSheet(tileSprites[x]).get_image(0, tileDim, tileDim, tileScale, (0,0,0)))
