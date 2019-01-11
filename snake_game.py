#Snake Game

#Game imports
import pygame
import sys
import random
import time


#Check for initializing errors
check_errors = pygame.init()
if check_errors[1] > 0:#prints number of errors if any
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:#if no errors
    print("(+) PyGame successfully initialized!")

#Play surface
playSurface = pygame.display.set_mode((720, 460))#set width and height of window
pygame.display.set_caption('Snake game!')#title of the window

#Colors
red = pygame.Color(255, 0, 0)#game over
green = pygame.Color(0, 255, 0)#snake
black = pygame.Color(0, 0, 0)#score
white = pygame.Color(255, 255, 255)#background
brown = pygame.Color(165, 42, 42)#food

#FPS controller
fpsController = pygame.time.Clock()

#Important varibles
snakePos = [100, 50]#coordinates of the head (make sure it is less than the playSurface size)
snakeBody = [[100,50], [90,50], [80,50]]#coordinates for the 3 starting body pieces

#Generates random food position
foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]#*10 makes it a number divisible by ten so the snake can collide
foodSpawn = True#know if you spawned a new food or not

#Initializes the direction the snake travels
direction = 'RIGHT'
changeto = direction

#Score
score = 0

#Game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)#grabs font from the system for the 'Game Over' label
    GOsurf = myFont.render('Game over!', True, red)#text saying, anti-aliasing on/off, color variable
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)#coordinates of the 'Game Over'
    playSurface.blit(GOsurf,GOrect)
    showScore(0)#shows the score in the middle
    pygame.display.flip()#updates the fps so it can display the words
    
    time.sleep(4)#waits four second before closing
    pygame.quit()#pygame exit
    sys.exit()#console exit

#Scoring function    
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score : {0}'.format(score) , True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:#displays it top left
        Srect.midtop = (80, 10)
    else:#displays it in the middle when the game is over
        Srect.midtop = (360, 120)
    playSurface.blit(Ssurf,Srect)
    
    
#Main Logic of the game
while True:
    for event in pygame.event.get():#gives a list of events in pygame events
        if event.type == pygame.QUIT:#checks type of the event to the quit type found in pygame
            pygame.quit()#closes pygame window
            sys.exit()#closes console
        elif event.type == pygame.KEYDOWN:#checking for keypress
            if event.key == pygame.K_RIGHT or event.key == ord('d'):#right arrow key or d
                changeto = 'RIGHT' 
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeto = 'LEFT' 
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeto = 'UP' 
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeto = 'DOWN' 
            if event.key == pygame.K_ESCAPE:#esc key
                pygame.event.post(pygame.event.Event(pygame.QUIT))#create event to quit the game when esc is pressed

    #Validation of direction (makes sure you can't go backwards/move into yourself)
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    #Update snake position [x,y]
    if direction == 'RIGHT':#adds ten to the x coordinate for the snake head to move it right
        snakePos[0] += 10
    if direction == 'LEFT':#left
        snakePos[0] -= 10
    if direction == 'UP':#up
        snakePos[1] -= 10
    if direction == 'DOWN':#down
        snakePos[1] += 10
    
    
    #Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:#if the snake head and the food have the same x,y
        score += 1
        foodSpawn = False#then the food will diappear
    else:
        snakeBody.pop()
        
    #Food Spawn
    if foodSpawn == False:#generates new food after the last one is eaten
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] 
    foodSpawn = True
    
    #Background
    playSurface.fill(white)
    
    #Draw Snake 
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
    
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0],foodPos[1],10,10))
    
    #Checks for boundaries
    if snakePos[0] > 710 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()
        
    #Self hit
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()
    
    #Common stuff
    showScore()
    pygame.display.flip()#updates the screen
    
    fpsController.tick(24)#fps (control the speed) (24)
