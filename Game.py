
import pygame
import random
import sys
from pygame.locals import *

level = input('Level[0/1/2/3]: ')

#Create the objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #load the plane image
        self.image = pygame.image.load('plane.png').convert()
        #remove the background of the image
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('bullet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        #define the generate position of bullets
        self.rect = self.image.get_rect(center=(470, random.randint(0, 700)))
        #change the speed according to the level user choosed
        if level == 0:
            self.speed = random.randint(1, 2)
        if level == 1:
            self.speed = random.randint(2, 3)
        if level == 2:
            self.speed = random.randint(3, 6)
        if level == 3:
            self.speed = random.randint(5, 7)

    def update(self):
        #make the bullet move from left to right
        self.rect.move_ip(-self.speed, 0)
        #to avoid the bullet vanished immediately when reaching the screen boundary
        #the bullet image will be removed after the whole image crossed the right border         #of the screen 
        if self.rect.right < 0:
            self.kill()

class Present(pygame.sprite.Sprite):
    def __init__(self):
        super(Present, self).__init__()
        self.image = pygame.image.load('Present.png').convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(0, 450),0))
        self.speed = random.randint(1, 3)
        
    def update(self):
        #make the supplies drop vertically with a random speed
        self.rect.move_ip(0, self.speed)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        #convert_alpha() works when the background is transparent
        self.image = pygame.image.load('cloud.png').convert_alpha()
        self.rect = self.image.get_rect(center = (470,random.randint(0,700)))

    def update(self):
        self.rect.move_ip(-1,0)
        if self.rect.right < 0:
            self.kill()

#define the main game into a function to make it recallable
def run_game():
    #Initialize the game
    pygame.init()
    #Set a screen of 450*700 and filled it with black
    screen = pygame.display.set_mode((450, 700),0,32)
    background = pygame.Surface(screen.get_size())
    background.fill((135, 208, 240))
    #Write a title
    pygame.display.set_caption("Get as much supply as you can :)")
    #Load a game over image
    game_over = pygame.image.load('gameover.png')
    #Create custom events for adding new objects periodically
    ADDENEMY = pygame.USEREVENT + 1
    #Adjust the time interval of generating the bullets according to the level 
    if level == 0:
        pygame.time.set_timer(ADDENEMY, 500)
    elif level == 3:
        pygame.time.set_timer(ADDENEMY, 150)
    else:
        pygame.time.set_timer(ADDENEMY, 250)
    ADDPRESENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDPRESENT, 1000)
    ADDCLOUD = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDCLOUD,2000)
    #Create a plane(player)
    player = Player()
    #Set the initial score
    score = 0
    #Set the initial player state
    hit = False
    #Create different group for different object
    bullet_list = pygame.sprite.Group()
    present_list = pygame.sprite.Group()
    clouds_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(player)
    
    clock = pygame.time.Clock()
    
    #The main loop
    #Checking the player state
    while not hit:
        #control the frame time
        clock.tick(60)
        #trigger the custom events, add objects to the world
        for event in pygame.event.get():
            if event.type == ADDENEMY:
                new_item = Bullet()
                bullet_list.add(new_item)
                all_sprites_list.add(new_item)
            elif event.type == ADDPRESENT:
                new_present = Present()
                present_list.add(new_present)
                all_sprites_list.add(new_present)
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds_list.add(new_cloud)
                all_sprites_list.add(new_cloud)
        #Blit the screen
        screen.blit(background, (0, 0))
        #Get the mouse position 
        position = pygame.mouse.get_pos()
        #Relate the mouse position to the plane position
        player.rect.x = position[0]
        player.rect.y = position[1]
        player.update()
        all_sprites_list.update()
        #blit all of the objects
        for all in all_sprites_list:
            screen.blit(all.image, all.rect)
        #Check for collision
        #if player and bullets collides
        #kill the player & jump out of the main loop 
        if pygame.sprite.spritecollideany(player, bullet_list):
            player.kill()
            hit = True
        #if player and supplies collides, add 1 point to the score variable
        if pygame.sprite.spritecollide(player, present_list, True):
            score += 1
        #we don't want any interaction between clouds and player, so we don't test the           #collides between them
        #set the font of the score board
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render('Score: '+ str(score), True, (128, 128, 128))
        #set the position of the score board
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        #blit the score board
        screen.blit(score_text, text_rect)
        #update the whole screen
        pygame.display.flip()
    #blit the gameover image and the final score
    font = pygame.font.Font(None, 45)
    text1 = font.render('Score: '+ str(score), True, (255, 0, 0))
    text1_rect = text1.get_rect()
    text1_rect.centerx = screen.get_rect().centerx
    text1_rect.centery = screen.get_rect().centery + 60
    text2 = font.render('Press r to restart', True, (255, 0, 0))
    text2_rect = text2.get_rect()
    text2_rect.centerx = screen.get_rect().centerx
    text2_rect.centery = screen.get_rect().centery + 100
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(game_over, (0, 0))

run_game()

while 1:
    for event in pygame.event.get():
        #check for the event that player wants to quit the game
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            #check for the event(press r key) that player wants to restart the game
            if event.key == K_r:
                run_game()
    pygame.display.update()
