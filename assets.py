import pygame, os

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

swidth = 960
sheight = 576
screen = pygame.display.set_mode((swidth,sheight))

playerBaseDim = 24
playerScale = 4

# player location indices
ppx = (swidth-playerBaseDim*playerScale)/2
ppy = (sheight-playerBaseDim*playerScale)/2
# walking animation control
walkingFrame = 4
walkingInterim = walkingFrame
playerFacingR = True

# right facing player sprites
playerSpriteImg = pygame.image.load("doux.png").convert_alpha()
playerSpriteSheet = SpriteSheet(playerSpriteImg)

playerFrames = []
for x in range(0,23):
    playerFrames.append(
        playerSpriteSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# left facing player sprites (inverted)
playerSpriteInv = pygame.transform.flip(playerSpriteImg, True, False)
playerSpriteInvSheet = SpriteSheet(playerSpriteInv)

playerInvFrames = []
for x in range(23,-1,-1):
    playerInvFrames.append(
        playerSpriteInvSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# tile square assets for map
tileScale = int((3/2)*playerScale)
tileDim = 16
tileSprites = []
path = "C:/Users/alvin/Desktop/PyGame/PyGame-First/MapAssets/Tiles"
dirlist = os.listdir(path)
for x in range(len(dirlist)):
    tileSprites.append(pygame.image.load(
        f"MapAssets/Tiles/{dirlist[x]}"
    ).convert_alpha())

tileList = []
for x in range(len(tileSprites)):
    tileList.append(
        SpriteSheet(tileSprites[x]).get_image(
            0, tileDim, tileDim, tileScale, (0,0,0)
        )
    )
