import pygame
import random

pygame.init()

screenSize = 400
screen = pygame.display.set_mode((screenSize, screenSize))

font = pygame.font.Font(None, 40)
buttonFont = pygame.font.Font(None, 20)

gridSize = 10   
squareSize = screenSize // gridSize
lightGrassColour = (76, 187, 23)
darkGrassColour = (0, 100, 0)
lightDirtColour = (92, 64, 32)
darkDirtColour = (79, 49, 10)

mineGrid = []
mineRarity = 0
adjacentMinesGrid = []
playerGrid = []

flagImage = pygame.image.load('flag.png').convert_alpha()
image = pygame.Surface((106, 113)).convert_alpha()
image.blit(flagImage, (0, 0))
image.set_colorkey((255, 255, 255))
circleImage = image

def setUpGame():
    global notMined
    global mineGrid
    global adjacentMinesGrid
    global playerGrid
    global gameOver
    global mineRarity

    mineGrid = []
    adjacentMinesGrid = []
    playerGrid = []
    gameOver = None

    row = []
    for y in range(gridSize):
        for x in range(gridSize):
            if random.randint(1, mineRarity) == 1:
                row.append(1)
            else:
                row.append(0)
                    
        mineGrid.append(row)
        row = []

    for y in range(gridSize):
        for x in range(gridSize):
            row.append(0)
                    
        playerGrid.append(row)
        row = []
            
    notMined = 0
    for y in range(gridSize):
        for x in range(gridSize):
            if mineGrid[y][x] == 0:
                notMined += 1

    for y in range(gridSize):
        for x in range(gridSize):
            row.append(0)
                    
        adjacentMinesGrid.append(row)
        row = []

    for y in range(gridSize):
        for x in range(gridSize):
            count = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (0 <= y + dy < gridSize) and (0 <= x + dx < gridSize):
                        count += mineGrid[y + dy][x + dx]
            adjacentMinesGrid[y][x] = count

gameOver = None
def gameOverFunc(mine):
    if mine == 1:
        for y in range(gridSize):
            for x in range(gridSize):
                if mineGrid[y][x] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (x * squareSize + squareSize // 2, y * squareSize + squareSize // 2), squareSize // 4)

    else:
        for y in range(gridSize):
            for x in range(gridSize):
                if mineGrid[y][x] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (x * squareSize + squareSize // 2, y * squareSize + squareSize // 2), squareSize // 4)

    pygame.draw.rect(screen, (255, 0, 0), ((screenSize/2) - 50, (screenSize/2) + 35, 100, 40), 3)
    pygame.draw.rect(screen, (255, 255, 255), ((screenSize/2) - 47, (screenSize/2) + 38, 94, 34))

    text_surface = buttonFont.render("New Game", True, (255, 0, 0))
    screen.blit(text_surface, ((screenSize/2) - 35, (screenSize/2) + 47))

def revealAdjacentSquares(y, x):
    if playerGrid[y][x] == 0:
        playerGrid[y][x] = 1
        if adjacentMinesGrid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (0 <= y + dy < gridSize) and (0 <= x + dx < gridSize):
                        revealAdjacentSquares(y + dy, x + dx)

running = True
while running:
    screen.fill((255, 255, 255))

    if mineRarity != 0:
        for y in range(gridSize):
            for x in range(gridSize):
                if playerGrid[y][x] == 0:
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(screen, lightGrassColour, (x * squareSize, y * squareSize, squareSize, squareSize))
                    else:
                        pygame.draw.rect(screen, darkGrassColour, (x * squareSize, y * squareSize, squareSize, squareSize))
                elif playerGrid[y][x] == 1:
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(screen, lightDirtColour, (x * squareSize, y * squareSize, squareSize, squareSize))
                    else:
                        pygame.draw.rect(screen, darkDirtColour, (x * squareSize, y * squareSize, squareSize, squareSize))

                    if adjacentMinesGrid[y][x] != 0:
                        text = font.render(str(adjacentMinesGrid[y][x]), True, (30, 144, 255))
                        screen.blit(text, ((x * squareSize) + 12 , (y * squareSize) + 9))
                elif playerGrid[y][x] == 2:
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(screen, lightGrassColour, (x * squareSize, y * squareSize, squareSize, squareSize))
                    else:
                        pygame.draw.rect(screen, darkGrassColour, (x * squareSize, y * squareSize, squareSize, squareSize))

                    if gameOver == None:
                        screen.blit(flagImage, ((x * squareSize) + 10 , (y * squareSize) + 8))

    else:
        text_surface = font.render("Choose Difficulty", True, (255, 0, 0))
        screen.blit(text_surface, ((screenSize/2) - 105, (screenSize/2) - 80))

        pygame.draw.rect(screen, (255, 0, 0), ((screenSize/2) - 50, (screenSize/2) - 40, 100, 40), 3)
        pygame.draw.rect(screen, (255, 255, 255), ((screenSize/2) - 47, (screenSize/2) - 37, 94, 34))
        text_surface = buttonFont.render("Easy", True, (255, 0, 0))
        screen.blit(text_surface, ((screenSize/2) - 35, (screenSize/2) - 30))

        pygame.draw.rect(screen, (255, 0, 0), ((screenSize/2) - 50, (screenSize/2) + 10, 100, 40), 3)
        pygame.draw.rect(screen, (255, 255, 255), ((screenSize/2) - 47, (screenSize/2) + 13, 94, 34))
        text_surface = buttonFont.render("Medium", True, (255, 0, 0))
        screen.blit(text_surface, ((screenSize/2) - 35, (screenSize/2) + 20))

        pygame.draw.rect(screen, (255, 0, 0), ((screenSize/2) - 50, (screenSize/2) + 60, 100, 40), 3)
        pygame.draw.rect(screen, (255, 255, 255), ((screenSize/2) - 47, (screenSize/2) + 63, 94, 34))
        text_surface = buttonFont.render("Hard", True, (255, 0, 0))
        screen.blit(text_surface, ((screenSize/2) - 35, (screenSize/2) + 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()

            if mineRarity != 0:
                if event.button == 1:
                    if gameOver == None:
                        for y in range(gridSize):
                            for x in range(gridSize):
                                if (((mouseX > x * squareSize) and (mouseX < (x * squareSize) + squareSize)) and ((mouseY > y * squareSize) and (mouseY < (y * squareSize) + squareSize))):
                                    if playerGrid[y][x] != 2:    
                                        if mineGrid[y][x] != 1:
                                            revealAdjacentSquares(y, x)
                                        else:
                                            gameOver = 1
                    else:
                        if ((mouseX > (screenSize/2) - 50) and mouseX < ((screenSize/2) - 50) + 100) and ((mouseY > (screenSize/2) + 35) and mouseY < ((screenSize/2) + 35) + 40):
                            setUpGame()

                elif event.button == 3:
                    if gameOver == None:
                        for y in range(gridSize):
                            for x in range(gridSize):
                                if (((mouseX > x * squareSize) and (mouseX < (x * squareSize) + squareSize)) and ((mouseY > y * squareSize) and (mouseY < (y * squareSize) + squareSize))):
                                    if playerGrid[y][x] == 0:
                                        playerGrid[y][x] = 2
                                    elif playerGrid[y][x] == 2:
                                        playerGrid[y][x] = 0

            else:
                if ((mouseX > (screenSize/2) - 50) and mouseX < ((screenSize/2) - 50) + 100) and ((mouseY > (screenSize/2) - 40) and mouseY < ((screenSize/2) - 40) + 40):
                    mineRarity = 15
                    setUpGame()
                elif ((mouseX > (screenSize/2) - 50) and mouseX < ((screenSize/2) - 50) + 100) and ((mouseY > (screenSize/2) + 10) and mouseY < ((screenSize/2) + 10) + 40):
                    mineRarity = 10
                    setUpGame()
                elif ((mouseX > (screenSize/2) - 50) and mouseX < ((screenSize/2) - 50) + 100) and ((mouseY > (screenSize/2) + 60) and mouseY < ((screenSize/2) + 60) + 40):
                    mineRarity = 7
                    setUpGame()

    if mineRarity != 0:
        revealed = 0
        for y in range(gridSize):
            for x in range(gridSize):
                if playerGrid[y][x] == 1:
                    revealed += 1
                    
        if revealed == notMined:
            gameOver = 0

        if gameOver == 0:
            gameOverFunc(gameOver)
        elif gameOver == 1:
            gameOverFunc(gameOver)

    pygame.display.update()
pygame.quit()