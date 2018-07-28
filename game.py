import pygame
import os
import time
import sys
import math
HEIGHT = 720
WIDTH = 1280

entity_list = []
character_list = []
projectile_list = []

class Entity:
    def __init__(self, position, velocity, picture):
        self.picture = picture
        self.velocity = velocity
        self.picture = pygame.image.load(picture)
        initPosition = position
        self.position = self.picture.get_rect()
        self.position = self.position.move(initPosition)
        self.sub_pixel = [0,0]
        entity_list.append(self)
    def out_of_bounds(self):
        if self.position.left < 0:
            return True
        if self.position.right > WIDTH:
            return True
        if self.position.bottom > HEIGHT:
            return True
        if self.position.top < 0:
            return True

class Player_Char(Entity):
    def __init__(self):
        Entity.__init__(self, [300, 300], [0,0], "Untitled.bmp")
        self.cool_down = 0
        character_list.append(self)
    def out_of_bounds(self):
        if self.position.left < 0:
            self.position.left = 0
        if self.position.right > WIDTH:
            self.position.right = WIDTH
        if self.position.bottom > HEIGHT:
            self.position.bottom = HEIGHT
        if self.position.top < 0:
            self.position.top = 0
        else:
            return False
        
class Bullet(Entity):
    def __init__(self, start_location, velocity, picture):
        Entity.__init__(self, start_location, velocity, picture)
        projectile_list.append(self)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()
pygame.display.set_caption('Bleep blorking game')
dude = Player_Char()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

def gameLoop():
    global dudeCoords
    while 1:
        for event in pygame.event.get():
            dude.velocity = [0,0]
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                dude.velocity[1] -= 5
            if pressed[pygame.K_s]:
                dude.velocity[1] += 5
            if pressed[pygame.K_a]:
                dude.velocity[0] -= 5
            if pressed[pygame.K_d]:
                dude.velocity[0] += 5
            elif event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseCoords = pygame.mouse.get_pos()
                fire(dude.position.center, mouseCoords)
        updateEntities()
        time.sleep(0.01666)

def updateEntities():
    screen.blit(background, [0,0])
    for entity in projectile_list:
        #screen.blit(background, entity.position)
        entity.position = entity.position.move(entity.velocity)
        entity.sub_pixel[0] += entity.velocity[0] % 1
        entity.sub_pixel[1] += entity.velocity[1] % 1
        if math.fabs(entity.sub_pixel[0]) > 0 or math.fabs(entity.sub_pixel[1]) > 0:
            entity.position = entity.position.move(entity.sub_pixel)
            entity.sub_pixel[0] %= 1
            entity.sub_pixel[1] %= 1
        if entity.out_of_bounds():
            entity = None
        else:
            screen.blit(entity.picture, entity.position)
        #print(entity.position, entity.velocity)
    for entity in character_list:
        #screen.blit(background, entity.position)
        entity.position = entity.position.move(entity.velocity)
        entity.out_of_bounds()
        screen.blit(entity.picture, entity.position)
    dude.cool_down -= 1

    pygame.display.flip()
def fire(start, end):
    if dude.cool_down <= 0:
        speed = 5
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        c = math.sqrt(dx * dx + dy * dy)
        
        #ratio = (math.sqrt(math.fabs((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)))/10
        velocity = [(speed * dx)/c, (speed * dy) / c]
        print(start, velocity)
        Bullet(start, velocity, 'bullet.bmp')
        dude.cool_down = 20

screen.blit(background, [0,0])
updateEntities()
pygame.display.flip()
gameLoop()
