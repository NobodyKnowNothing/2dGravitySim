import pygame
import pygame.font
import sys
import math
from random import randrange, uniform

from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

G = pow(6.674*10, -11)
HEIGHT = 1000
WIDTH = 1920
ACC = 0.05
FRIC = 0 
FPS = 60
colTog = False
gravTog = False
pausTog = False

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity")


class Object(pygame.sprite.Sprite):
    
    def __init__(self, pos):
        super().__init__()

        self.clip = False
        self.check = 0
        self.mass = float(pow(10, 20))
        self.rad = 2
        self.pos = vec(pos)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.surf = pygame.Surface((self.rad*2, self.rad*2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (128,255,40), (self.rad, self.rad), self.rad, 0)
        self.rect = self.surf.get_rect(center = self.pos)
    
    def physics(self):
        global colTog, G, gravTog, ACC, pausTog
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            all_sprites.remove(self)
                
        if self.pos.x > WIDTH + self.rad:
            self.pos.x = 0
            self.vel = self.vel*0.95
        if self.pos.x < 0 - self.rad:
            self.pos.x = WIDTH
            self.vel = self.vel*0.95
        if self.pos.y > HEIGHT + self.rad:
            self.pos.y = 0
            self.vel = self.vel*0.95
        if self.pos.y < 0 - self.rad:
            self.pos.y = HEIGHT
            self.vel = self.vel*0.95
        
        if pausTog == False:   
            for entity in all_sprites:
                if entity != self:
                    dx, dy = entity.rect.center[0] - self.rect.center[0], entity.rect.center[1] - self.rect.center[1]
                    dist = math.hypot(dx, dy)
                    try:
                        dx, dy = dx / dist, dy / dist
                    except:
                        dist = 1
                        dx, dy = dx / dist, dy / dist
                    if (self.rad + entity.rad) < dist and gravTog == False:
                        F = (G*(self.mass * entity.mass))/(dist**2)
                        A = F/self.mass
                        self.acc += vec(dx, dy) * A
                    if (self.rad + entity.rad) > dist:
                        if colTog:
                            tempv = vec(self.vel)
                            self.check += 1
                            self.vel = (vec((self.mass-entity.mass)*self.vel) + vec(entity.vel*entity.mass*2))/(self.mass+entity.mass)
                            entity.vel = (((self.mass*2)/(self.mass+entity.mass))*tempv)+((entity.mass-self.mass)/(self.mass+entity.mass))*self.vel
                            
                        elif self.mass >= entity.mass:
                            self.vel = ((self.mass*self.vel) + (entity.mass*entity.vel))/(self.mass+entity.mass)
                            self.mass = self.mass + entity.mass
                            self.rad = ((((self.rad**2)*math.pi) + ((entity.rad**2)*math.pi))/math.pi)**0.5
                            self.surf = pygame.transform.scale(self.surf, ((self.rad)*2, (self.rad)*2))
                            self.rect = self.surf.get_rect(center = self.pos)
                            self.surf.fill((255,255,255,0))
                            all_sprites.remove(entity)
                            pygame.draw.circle(self.surf, (128,255,40), (self.rad, self.rad), self.rad, 0)
            if self.clip == False and self.check > 0:
                self.check = 0
            self.clip = False
                            
                                                    
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if keys[pygame.K_LEFT]:
                    self.acc.x += -ACC
                    print(self.acc)
                if keys[pygame.K_RIGHT]:
                    self.acc.x += ACC
                    print(self.acc)
                if keys[pygame.K_UP]:
                    self.acc.y += -ACC
                    print(self.acc)
                if keys[pygame.K_DOWN]:
                    self.acc.y += ACC
                    print(self.acc)
                if keys[pygame.K_z]:
                    self.acc = vec(0,0)
                    self.vel = vec(0,0)
                    print(self.acc)
            

                        
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
                        
            self.rect.center = self.pos

            if pausTog == False:
                self.acc = vec(0,0)

all_sprites = pygame.sprite.Group()

def main():
    global colTog, G, gravTog, pausTog
    ptogwait = 0
    gravtogwait = 0
    ctogwait = 0
    while True:
        displaysurface.fill((0,0,0))
        if pygame.font:
            font = pygame.font.Font(None, 30)
            text = font.render("Tab for collision change (Unfinished), Space to pause, G to toggle gravity, Hold left click to add mass. Hover mouse over objects and press Z to stop, arrow keys to change acceleration", True, (40, 40, 40))
            textpos = text.get_rect(centerx=displaysurface.get_width() / 2, y=10)
            displaysurface.blit(text, textpos)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
                obj = Object(pygame.mouse.get_pos())
                all_sprites.add(obj)

        # Controls, Tab = collision toggle, Space = physics toggle, Backspace = clear screen, G = gravity toggle
        if ptogwait > 0:
            ptogwait -= 1
        if gravtogwait > 0:
            gravtogwait -= 1
        if ctogwait > 0:
            ctogwait -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and ctogwait == 0:
            if colTog:
                colTog = False
                ctogwait = 10
            else:
                colTog = True
                ctogwait = 10
            print(f"Col: {colTog}")
        if keys[pygame.K_g] and gravtogwait == 0: 
            if gravTog:
                gravTog = False
                gravtogwait = 10
            else:
                gravTog = True
                gravtogwait = 10
            print(f"Grav: {gravTog}")
        if keys[pygame.K_SPACE] and ptogwait == 0:
            if pausTog:
                pausTog = False
                ptogwait = 10
            else:
                pausTog = True
                ptogwait = 10
            print(f"Paus: {pausTog}")
        for entity in all_sprites:
            entity.physics()
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)

main()
