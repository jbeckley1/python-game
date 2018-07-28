import pygame
import os
import time
import sys
import math
HEIGHT = 720
WIDTH = 1280

#lists to hold things
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
    def update_position(self):
        self.position = self.position.move(self.velocity)
        self.sub_pixel[0] += self.velocity[0] % 1
        self.sub_pixel[1] += self.velocity[1] % 1
        if math.fabs(self.sub_pixel[0]) > 0 or math.fabs(self.sub_pixel[1]) > 0:
            self.position = self.position.move(self.sub_pixel)
            self.sub_pixel[0] %= 1
            self.sub_pixel[1] %= 1

class Character(Entity):
    def __init__(self, starting_pos, picture_filename):
        Entity.__init__(self, starting_pos, [0,0], picture_filename)
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
        
class Player_Char(Character):
    def __init__(self):
        Character.__init__(self, [300, 300], "Untitled.bmp")
        self.is_firing = False
        
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
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                dude.is_firing = True
            if event.type == pygame.MOUSEBUTTONUP:
                dude.is_firing = False
            elif event.type == pygame.QUIT:
                pygame.quit()

        if dude.is_firing:
            mouseCoords = pygame.mouse.get_pos()
            fire(dude.position.center, mouseCoords)
            
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
        updateEntities()
        time.sleep(0.01666)

def updateEntities():
    screen.blit(background, [0,0])
    for entity in projectile_list:
        entity.update_position()
        if entity.out_of_bounds():
            entity = None
        else:
            screen.blit(entity.picture, entity.position)
    for entity in character_list:
        entity.update_position()
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
        velocity = [(speed * dx)/c, (speed * dy) / c]
        print(start, velocity)
        Bullet(start, velocity, 'bullet.bmp')
        dude.cool_down = 10

screen.blit(background, [0,0])
updateEntities()
pygame.display.flip()
gameLoop()
