import pygame
import os
import time
import sys
import math
import inspect
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
        if self.velocity[0] > 0:
            self.sub_pixel[0] += self.velocity[0] % 1
        elif self.velocity[0] < 0:
            self.sub_pixel[0] -= self.velocity[0] % 1
        if self.velocity[1] > 0:
            self.sub_pixel[1] += self.velocity[1] % 1
        elif self.velocity[1] < 0:
            self.sub_pixel[1] -= self.velocity[0] % 1
        

        if math.fabs(self.sub_pixel[0]) > 0 or math.fabs(self.sub_pixel[1]) > 0:
            self.position = self.position.move(self.sub_pixel)
        if self.sub_pixel[0] >= 0:
            self.sub_pixel[0] %= 1
        else:
            self.sub_pixel[0] = -(1 - self.sub_pixel[0] % 1)
            
        if self.sub_pixel[1] >= 0:
            self.sub_pixel[1] %= 1
        else:
            self.sub_pixel[1] = -(1 - self.sub_pixel[1] % 1)

class Character(Entity):
    def __init__(self, starting_pos, picture_filename):
        Entity.__init__(self, starting_pos, [0,0], picture_filename)
        self.cool_down = 0
        self.health = 1
        self.is_enemy = False
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
        
    def collision_detect(self):
        for bullet in projectile_list:
            if bullet.is_enemy_bullet != self.is_enemy:                    
                if(bullet.position.center[0] > self.position.left and bullet.position.center[0] < self.position.right):
                    if(bullet.position.center[1] > self.position.top and bullet.position.center[1] < self.position.bottom):
                       projectile_list.remove(bullet)
                       self.take_damage(bullet.damage)
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def die(self):
        character_list.remove(self)

class Enemy(Character):
    def __init__(self, starting_pos):
        Character.__init__(self, starting_pos, "Enemy.png")
        self.path_counter = 0
        self.health = 5
        self.path_radius = 4
        self.is_enemy = True
    def path(self):
        self.velocity = [self.path_radius * math.cos(math.radians(self.path_counter)), self.path_radius * math.sin(math.radians(self.path_counter))]
    def update_position(self):
        self.path_counter += 10
        self.path()
        super().update_position()

class Player_Char(Character):
    def __init__(self):
        Character.__init__(self, [300, 300], "Untitled.bmp")
        self.is_enemy = False
        self.is_firing = False
        self.health = 10
        self.top_speed = 5
        # The rate at which you gain speed
        self.acceleration = 2

    def limit_speed(self):
        if self.velocity[0] > self.top_speed:
            self.velocity[0] = self.top_speed
        if self.velocity[1] > self.top_speed:
            self.velocity[1] = self.top_speed
        if self.velocity[0] < -self.top_speed:
            self.velocity[0] = -self.top_speed
        if self.velocity[1] < -self.top_speed:
            self.velocity[1] = -self.top_speed
        
class Bullet(Entity):
    def __init__(self, start_location, velocity, picture):
        Entity.__init__(self, start_location, velocity, picture)
        self.damage = 1
        self.is_enemy_bullet = False
        projectile_list.append(self)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()
pygame.display.set_caption('Bleep blorking game')
dude = Player_Char()
enemy = Enemy([500,500])
enemy2 = Enemy([1000,300])
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

enemy_type_dict = {"Circle_Enemy" : Enemy}

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
            
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            dude.velocity[1] -= dude.acceleration
        elif dude.velocity[1] < 0:
            dude.velocity[1] += dude.acceleration // 2
        if pressed[pygame.K_s]:
            dude.velocity[1] += dude.acceleration
        elif dude.velocity[1] > 0:
            dude.velocity[1] -= dude.acceleration // 2
        if pressed[pygame.K_a]:
            dude.velocity[0] -= dude.acceleration
        elif dude.velocity[0] < 0:
            dude.velocity[0] += dude.acceleration // 2
        if pressed[pygame.K_d]:
            dude.velocity[0] += dude.acceleration
        elif dude.velocity[0] > 0:
            dude.velocity[0] -= dude.acceleration // 2
        dude.limit_speed()
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
        entity.collision_detect()
        screen.blit(entity.picture, entity.position)
    dude.cool_down -= 1
    pygame.display.flip()

                        
def fire(start, end):
    if dude.cool_down <= 0:
        speed = 10
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        c = math.sqrt(dx * dx + dy * dy)
        velocity = [(speed * dx)/c, (speed * dy) / c]
        #print(start, velocity)
        Bullet(start, velocity, 'bullet.bmp')
        dude.cool_down = 10

screen.blit(background, [0,0])
updateEntities()
pygame.display.flip()
gameLoop()
