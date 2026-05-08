import pygame
import random
import math
from pygame import mixer

#initialize pygame to acces cool methods in pygame
pygame.init()

# create screen
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load('background1.png')

#Title and icon
pygame.display.set_caption("Attack Aliens")
icon= pygame.image.load('spaceship.png') #here in icon variable ufo.png is stored
pygame.display.set_icon(icon) # it will display icon 

#player
playerimg=pygame.image.load('arcade-game.png')
playerx=370 #player image from x axis
playery=480 #player image from y axis
playerx_change=0

#enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_of_enemy=5
for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0,800)) #enemy image from x axis
    enemyy.append(random.randint(50,150)) #enemy image from y axis
    enemyx_change.append(2)
    enemyy_change.append(20) #enemy will move in y direction also

#bullet 
bulletimg=pygame.image.load('bullet.png')
bulletx=0 #bullet image from x axis
bullety=480 #bullet image from y axis
bulletx_change=0 # here bullet is not changing in x direction
bullety_change=16 #bullet will move in y direction also
bullet_state="ready" #here ready state means u cant see bullet
                    # here fire will mean bullet is moving
#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score=font.render("Killed:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y)) 

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def  player(x,y):
    screen.blit(playerimg,(x,y)) #using this method we gonna draw player image on screen

def  enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y)) #using this method we gonna draw player image on screen

def fire_bullet(x,y):#this is made and used when bullet is fired
    global bullet_state  #global is used so it can access from outside function
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))  #bullet image will be drawna and will appear on x,y coordinate

def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:  # Adjust the collision threshold if necessary
        return True
    else:
        return False

#game loop
running=True
while running:
  
    #RGB colors
    screen.fill((0,0,0)) 
    #background image
    screen.blit(background,(0,0)) #screen.blit will draw image
    
    for event in pygame.event.get(): #It returns a list of event objects that represent all the events currently in the event queue.
        if event.type==pygame.QUIT:   #Each event object has a type attribute that indicates the kind of event (e.g., QUIT, KEYDOWN, MOUSEBUTTONDOWN, etc.).
           running=False

        # if key stroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change= -4
            if event.key == pygame.K_RIGHT:
                playerx_change= 4
            if event.key ==pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletx=playerx # when as soon as space is pressed current value of player is stored and saved in bulletx value.
                    fire_bullet(bulletx,bullety)
                      

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change= 0
            
        
    

    
    playerx +=playerx_change
# to make boundaries for rocket not to go beyond screen
    if playerx <=0:
        playerx=0
    elif playerx >=736:
        playerx = 736
        
#  enemy movement
    for i in range(num_of_enemy):

        # Game Over
        if enemyy[i] > 440:
            for j in range(num_of_enemy):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] +=enemyx_change[i]
# to make boundaries for enemy not to go beyond screen
        if enemyx[i] <=0:
            enemyx_change[i]=3 # when enemy hits -ve x direction then it should move towrads +ve direction
            enemyy[i]+= enemyy_change[i]
         
        elif enemyx[i] >=736:
            enemyx_change[i] = -3
            enemyy[i]+= enemyy_change[i]
        
    #collision
        collision=iscollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play() 
            bullety=480
            bullet_state= "ready"
            score_value +=1
            
            enemyx[i]=random.randint(0,800) #enemy image from x axis
            enemyy[i]=random.randint(50,150) #enemy image from y axis
            
        enemy(enemyx[i],enemyy[i],i)



 #bullet movement
    if bullety<=0: # if bullet goes beyond y coordinate i.e beyond screen
        bullety=480 #this valye reset bullet to original
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletx,bullety) #x coordinate of spaceship i.e bullet will start from  spaceship and y direction for bullet movemnet up
        bullety-= bullety_change




    player(playerx,playery)
    show_score(textx,texty)
    
    pygame.display.update() # it will display with color fill.As it update the changes done on screenif slow the speed of enemy movement change in this code only 