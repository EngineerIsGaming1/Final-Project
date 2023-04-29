import numpy as np
import pygame
import time

# Primary class used to make the game work
# Functions like a button on screen that draws itself and changes attribute "clicked"
# to true when a player clicks its location
class lineButton:
    # Constructor inputs:
    # x,y: x,y location on the screen of class
    # dimensions: a tuple containing the length and width of the class
    # gameDisplay: a pygame object that represents the pygame window
    def __init__(self, x, y, dimensions, gameDisplay):
        self.rect = pygame.Rect((x,y), dimensions) 
        # creates a pygame object "Rect". Passed values of (x,y) and dimensions (a tuple containing (length, width))
        # determine location of topleft of rectangle and shape
        self.display = gameDisplay
        self.clicked = False

    # draws the rectangle with given color
    def draw(self, color):
        pygame.draw.rect(self.display, color, self.rect)
        pygame.display.flip()

# Function used to see if users cliked the pygame window's "X" at any time
def checkQuit(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
    
    return(running)

# Function used to check if all elements of inputBox have been clicked
def checkBox(inputBox):
    clickedBox = []
    [clickedBox.append(curLine.clicked) for curLine in inputBox]

    return(all(clickedBox)) # all() returns True if all elements inside the given iterable are True

# Function used to calculate any points gained by player action    
def checkPoints(line, boxes):
    score = 0

    for curBox in boxes:
        if line in curBox:
            score += checkBox(curBox)

    return(score)


# Basic player action. "color" is used to represent which player took which action
def playerAction(boxes, color):
    action = True
    
    while action:
        # This quit action has to be in any while loop or else pygame gets mad and crashes
        # Exiting before the main gameloop ends will intentionally report an error
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cleanupSequence()

        mousePos = pygame.mouse.get_pos() # gets mouse position using get_pos()
        
        # Nested for loop that indexes through individual elements of the list of boxes
        for curBox in boxes:
            for curLine in curBox:
                # "rect" object has an attribute "collidepoint" that returns true or false based on the coordinates given
                if curLine.rect.collidepoint(mousePos):
                    # if mouse is clicked and the clicked object hasn't been clicked yet, draw it and check if any new points have been scored
                    # statement waits .25s after completed action to ensure doubleclicks aren't registered
                    if pygame.mouse.get_pressed()[0] == 1 and curLine.clicked == False:
                        curLine.clicked = True
                        curLine.draw(color)
                        points = checkPoints(curLine, boxes)
                        action = False
                        time.sleep(.25)

    return(points)

# StartupSequence sets up the playing board and returns an array of buttons that represent the possible player moves.
def startupSequence(rows, cols, size, display):
    # numpy's linspace used to split the playing area evenly.
    rowArray = np.linspace(0, size[1], num = (rows + 2))
    rowArray = rowArray[1:-1] # These lines remove the edges of the linspace equation
    colArray = np.linspace(0, size[0], num = (cols + 2))
    colArray = colArray[1:-1]
    buttonArrayHoriz = []
    buttonArrayVert = []
    boxList = []

    # Fills the display with white, then draws the dots onto the screen
    display.fill("white")
    [[pygame.draw.circle(display, "black", (dotCol, dotRow), 10) for dotCol in colArray] for dotRow in rowArray]
    # how function works -> pygame.draw.circle(surface, color, (center location in tuple), radius)

    # creates a list of horizontal buttons. Indexes like matlab when only 1 dimension is given
    [[buttonArrayHoriz.append(lineButton(colArray[b] , rowArray[i] - 3, (colArray[b + 1] - colArray[b], 9), display)) \
      for b in range(cols - 1)] for i in range(rows)]
            # colArray[b + 1] - colArray[b] determines rectangle length, "9" is just the width I chose
            # Must be careful, coordinates go (x,y) but matrices go (row, col) which is (y,x)
            # display is just the game screen

    # creates a list of vertical buttons. Indexes like matlab when only 1 dimension is given
    [[buttonArrayVert.append(lineButton(colArray[k] - 3, rowArray[j], (9, rowArray[j + 1] - rowArray[j]), display)) \
      for k in range(cols)] for j in range(rows - 1)]
    
    # creates a list of lists of all boxes in the playing area
    for z in range((rows - 1) * (cols - 1)):
        boxList.append([buttonArrayHoriz[z], buttonArrayVert[z + 1 + (z // (cols - 1))],\
                        buttonArrayHoriz[z + (cols - 1)], buttonArrayVert[z + (z // (cols - 1))]])

    pygame.display.flip() # pygame line that displays any changes made
    return(boxList)

# Function used when game has ended. Displays which player won and what their score is
def endGame(display, oneScore, twoScore, screenSize):
    display.fill("white")
    font = pygame.font.Font('freesansbold.ttf', 32)
    if oneScore > twoScore:
        # Code reused from # https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
        # Writes text in center of screen
        text = font.render(f'Player one wins! Score: {oneScore}', True, "black", "white")
        textRect = text.get_rect()
        textRect.center = (screenSize[0] // 2, screenSize[1] // 2)
        display.blit(text, textRect)
        pygame.display.update()
        time.sleep(3)
    elif twoScore > oneScore:
        text = font.render(f'Player two wins! Score: {twoScore}', True, "black", "white")
        textRect = text.get_rect()
        textRect.center = (screenSize[0] // 2, screenSize[1] // 2)
        display.blit(text, textRect)
        pygame.display.update()
        time.sleep(3)
    elif oneScore == twoScore:
        text = font.render(f'Tie game! Scores: {oneScore}', True, "black", "white")
        textRect = text.get_rect()
        textRect.center = (screenSize[0] // 2, screenSize[1] // 2)
        display.blit(text, textRect)
        pygame.display.update()
        time.sleep(3)
    
    
    

# Function used to exit game properly. pygame.quit() uninitializes all pygame stuff and closes the game window
def cleanupSequence():
    print("Quitting game\n")
    pygame.quit()

# MAIN FUNCTION STARTS BELOW
# V V V V V V V V V V

# do while loop that makes sure inputs are integers
while True:
    numRows = input("Enter the number of rows to play: ")
    numCols = input("Enter number of columns to play: ")

    if (numRows.isdigit() and numCols.isdigit()):
        if(int(numRows) > 2 and int(numCols) > 2):
            numRows = int(numRows)
            numCols = int(numCols)
            break
        else:
            print("Inputs must be greater than 2, try again\n")
    else:
        print("Inputs are not integers, try again\n")
        time.sleep(.25)

totalMoves = 0
gameClock = pygame.time.Clock()
playerOneScore = 0
playerTwoScore = 0

pygame.init() #pygame.init initializes game module
gameRunning = True
screenSize = (840, 600)
gameDisplay = pygame.display.set_mode(screenSize, pygame.HWSURFACE | pygame.DOUBLEBUF)
    # https://stackoverflow.com/questions/29135147/what-do-hwsurface-and-doublebuf-do
    # HWSURFACE -> hardware acceleration. DOUBLEBUF -> reduces artifacting by saving to vram
pygame.display.set_caption('Dots and Boxes')
boxList = startupSequence(numRows,numCols,screenSize, gameDisplay)

# The equation I use to see how many possible moves there are is: rows*(col-1) + cols*(rows-1) simplified
# This equation is used to end the gameloop once all possible moves have been made
while gameRunning:
    # Checks if the "X" button is clicked at any time
    # Required line for pygame to function properly
    gameRunning = checkQuit(gameRunning)

    # Nested if statments used to avoid the use of "break"
    if (totalMoves < (2 * (numRows * numCols) - numRows - numCols)):
        # Passing blue and red signifies the two different players' actions
        playerOneScore += playerAction(boxList, "Blue")
        totalMoves += 1
        if (totalMoves < (2 * (numRows * numCols) - numRows - numCols)):
            playerTwoScore += playerAction(boxList, "Red")
            totalMoves += 1
        else:
            gameRunning = False
    else:
        gameRunning = False

    gameClock.tick(60)

endGame(gameDisplay, playerOneScore, playerTwoScore, screenSize)
cleanupSequence()


# https://www.youtube.com/watch?v=G8MYGDf_9ho&t=879s
# https://www.pygame.org/docs/
