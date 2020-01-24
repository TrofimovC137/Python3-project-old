import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from random import randint
from math import *
#pygame.sprite.spritecollide столкновение
#pygame.mouse.get_pos()
class Object(Sprite):
    def __init__(self, screen, m, x, y, Vx, Vy,img_filename, speed,h):
        Sprite.__init__(self)
        self.m = m
        self.h = h
        self.grad = 0
        self.speed = speed
        self.x, self.y = x, y
        self.Vx, self.Vy = Vx, Vy
        self.animations = 0
        self.player = False
        self.Del = False
        self.base_image = pygame.image.load(img_filename)
        self.image = self.base_image
        self.screen = screen
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self,screen, time_passed,pVx,pVy):
        dt = time_passed/1000
        self.x += (self.Vx-pVx)*dt
        self.y += (self.Vy-pVy)*dt
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
    image = 0
    
class AnimationObject(Object,Sprite):
    def __init__(self, screen, x, y, Animation_List, fps, h, grad, cycle, material):
        Sprite.__init__(self)
        self.x, self.y = x, y
        self.animations = 0
        self.cycle = cycle
        self.grad = grad
        self.Hp = 0
        self.material=material
        self.player = False
        self.Del = False
        self.h = h
        self.fps = fps
        self.Vx, self.Vy = 0, 0
        self.Animation_List=[]
        for i in range (0,len(Animation_List)):
            self.Animation_List.append(pygame.image.load(Animation_List[i]))
        self.image = self.Animation_List[0]
        self.screen = screen
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self, screen, time_passed, pVx, pVy,Object_List,MyIndex):
        if (self.animations >= len(self.Animation_List)-1)and(self.cycle==True):
            self.animations = 0
        if (self.animations >= len(self.Animation_List)-1) and (self.cycle==False):
            self.Del = True
        self.image = self.Animation_List[ceil(self.animations)]
        self.animations+=self.fps
        self.image = pygame.transform.rotate(self.image, self.grad)
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        Object.update(self, screen, time_passed, pVx, pVy)
        return Object_List
class StaticAnimationObject(AnimationObject,Sprite):
    def __init__(self, screen, x, y, Animation_List, fps, h, grad, cycle, material):
        AnimationObject.__init__(self, screen, x, y, Animation_List, fps, h, grad, cycle, material)
    def update (self, screen, time_passed, pVx, pVy,Object_List,MyIndex):
        Object_List=AnimationObject.update(self, screen, time_passed, 0, 0,Object_List,MyIndex)
        return Object_List
class Turret(Object, Sprite):
    def __init__(self, screen, x, y, gSpeed, img_filename, h, lang, kd):
        self.gSpeed = gSpeed
        self.lang = lang
        self.h=h
        self.kd = kd
        self.ver = 100
        self.canon_grad = 0
        Object.__init__(self, screen, 0, x, y, 0, 0, img_filename, 0, 2)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self, screen, Xgoal, Ygoal, x, y, grad, canon_grad, Object_List,Fire):
        self.canon_grad=canon_grad
        if Xgoal-self.x==0:
            if Ygoal-self.y>0:
                grad_to_goal = 90
            else:
                grad_to_goal = 270
        elif Ygoal-self.y == 0:
            if Xgoal-self.x>0:
                grad_to_goal = 0
            else:
                grad_to_goal = 180
        else:
            grad_to_goal = atan(-(Ygoal-self.y)/(Xgoal-self.x))*57
        if Ygoal<self.y and Xgoal<self.x:
            grad_to_goal = 180+grad_to_goal
        elif Ygoal>self.y and Xgoal<self.x:
            grad_to_goal+=180
        elif Ygoal>self.y and Xgoal>self.x:
            grad_to_goal = 360+grad_to_goal
        if self.grad>360:
            self.grad-=360
        elif self.grad<0:
            self.grad=360+self.grad
        if fabs(grad_to_goal-self.grad)<self.gSpeed:
            self.grad+=(grad_to_goal-self.grad)
            self.image = pygame.transform.rotate(self.base_image, self.grad)
        elif self.grad<180:
            if grad_to_goal<self.grad or grad_to_goal>180+self.grad:
                self.grad-=self.gSpeed
                self.image = pygame.transform.rotate(self.base_image, self.grad)
            else:
                self.grad+=self.gSpeed
                self.image = pygame.transform.rotate(self.base_image, self.grad)
        else:
            if grad_to_goal>self.grad or self.grad-180>grad_to_goal:
                self.grad+=self.gSpeed
                self.image = pygame.transform.rotate(self.base_image, self.grad)
            else:
                self.grad-=self.gSpeed
                self.image = pygame.transform.rotate(self.base_image, self.grad)
        if fabs(grad_to_goal-self.grad)<self.gSpeed:
            self.grad+=(grad_to_goal-self.grad)
            self.image = pygame.transform.rotate(self.base_image, self.grad)
        self.x = x+self.lang*cos(grad/57)
        self.y = y-self.lang*sin(grad/57)
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
        if self.ver<100:
            self.ver+=self.kd
        if Fire == True and self.ver>=100:
            Object_List.append(Whizbang(screen,self.x, self.y,self.grad,self.canon_grad,['whizbang.png'],500*cos(self.canon_grad/57) , self.h+1, 10))
            Object_List.append(AnimationObject(screen, self.x+50*cos(self.grad/57), self.y+(-50*sin(self.grad/57)), ['flash1.png','flash2.png','flash3.png'],
                                               0.5,self.h+0.1,self.grad,False,False))
            self.ver-=100
        return Object_List
class Player(Object,Sprite):
    def __init__(self, screen, m, x, y, Vx, Vy,img_filename, speed, h,gSpeed, Turret_List, yvn):
        Object.__init__(self, screen, m, x, y, Vx, Vy,img_filename, speed, h)
        self.player = True
        self.Hp = 100
        self.Fire = False
        self.material = True
        self.yvn=yvn
        self.PermissibleSpeed = ['all','all']
        self.tabl = StaticAnimationObject(screen,180,653,['tabl.png'],0,1,0,True,False)
        self.IntGun = StaticAnimationObject(screen,75,758,['gun.png'],0,1,0,True,False)
        self.inter = StaticAnimationObject(screen,145,656,['inter.png'],0,1,0,True,False)
        self.Hp_List = []
        self.Kd_List = []
        for i in range(0,100):
            self.Hp_List.append(StaticAnimationObject(screen,20,758-i*2,['Hp.png'],0,1,0,True,False))
            self.Kd_List.append(StaticAnimationObject(screen,55,758-i*2,['Kd.png'],0,1,0,True,False))
        self.canon_grad = 0
        self.gSpeed = gSpeed
        self.Turret_List = Turret_List
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self,screen,time_passed,pVx,pVy,Object_List,MyIndex):
        keys = pygame.key.get_pressed()
        if self.grad>360:
            self.grad-=360
        elif self.grad<0:
            self.grad=360+self.grad
        if keys[K_UP]:
            self.Vx=self.speed*cos(self.grad/57)
            self.Vy=-self.speed*sin(self.grad/57)
        elif keys[K_DOWN]:
            self.Vx=-self.speed*cos(self.grad/57)
            self.Vy=self.speed*sin(self.grad/57)
        else:
            self.Vx = 0
            self.Vy = 0
        if (self.Vx>0 and self.PermissibleSpeed[0] == '-') or (self.Vx<0 and self.PermissibleSpeed[0] == '+'):
            self.Vx=0
        if (self.Vy>0 and self.PermissibleSpeed[1] == '-') or (self.Vy<0 and self.PermissibleSpeed[1] == '+'):
            self.Vy=0
        self.PermissibleSpeed = ['all','all']
        cont = False
        for i in range(0,len(Object_List)):
            if pygame.sprite.collide_mask(Object_List[MyIndex],Object_List[i])!=None and i!=MyIndex and fabs(self.h-Object_List[i].h)<1 and Object_List[i].material==True:
                if Object_List[i].x>self.x:
                    self.PermissibleSpeed[0]='-'
                else:
                    self.PermissibleSpeed[0]='+'
                if Object_List[i].y>self.y:
                    self.PermissibleSpeed[1]='-'
                else:
                    self.PermissibleSpeed[1]='+'
                cont = True
                break
        if cont == False:
            if keys[K_RIGHT]:
                self.grad-=self.gSpeed
            elif keys[K_LEFT]:
                self.grad+=self.gSpeed
        self.image = pygame.transform.rotate(self.base_image, self.grad)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image_w, self.image_h = self.image.get_size()
        screen.blit(self.image, self.rect)
        #обработка модулей
        self.inter.update(screen,time_passed,self.Vx,self.Vy,[],0)
        self.tabl.update(screen,time_passed,self.Vx,self.Vy,[],0)
        self.IntGun.grad = self.canon_grad
        self.IntGun.update(screen,time_passed,self.Vx,self.Vy,[],0)
        for i in range(0,self.Hp):
            self.Hp_List[i].update(screen,time_passed,self.Vx,self.Vy,[],0)
        for i in range(0,self.Turret_List[0].ver):
            self.Kd_List[i].update(screen,time_passed,self.Vx,self.Vy,[],0)
        i=0
        self.Fire = False
        if keys[K_EQUALS]:
            self.canon_grad+=0.5
        elif keys[K_MINUS]:
            self.canon_grad-=0.5
        if self.canon_grad<self.yvn[0]:
            self.canon_grad=self.yvn[0]
        elif self.canon_grad>self.yvn[1]:
            self.canon_grad=self.yvn[1]
        if pygame.mouse.get_pressed(0)[0]==1:
            self.Fire = True
        while i<=(len(self.Turret_List)-1):
            Object_List=self.Turret_List[i].update(screen, pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], self.x, self.y, self.grad,self.canon_grad,
                                                   Object_List, self.Fire)
            i+=1
        return Object_List
class Whizbang(Object,Sprite):
    def __init__(self, screen, x, y,grad,Vgrad,Animation_List, speed, h, damage):
        self.speed = speed
        self.x=x+37*cos(grad/57)
        self.y=y+(-37*sin(grad/57))
        self.Vx=self.speed*cos(grad/57)
        self.Vy=-self.speed*sin(grad/57)
        self.Vh=self.speed*sin(Vgrad/57)
        self.damage = damage
        self.Hp = 1
        self.material = True
        self.player = False
        self.Del = False
        self.animations = 0
        self.grad = grad
        self.fps = 0
        self.Animation_List=[]
        for i in range (0,len(Animation_List)):
            self.Animation_List.append(pygame.image.load(Animation_List[i]))
        self.image=self.Animation_List[0]
        self.h=h
        self.screen = screen
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()
    def update(self, screen, time_passed, pVx, pVy, Object_List, MyIndex):
        for i in range (0,len(Object_List)):
            if self.x>Object_List[i].x:
                if (pygame.sprite.collide_mask(Object_List[MyIndex],Object_List[i])!=None  and i!=MyIndex and self.h<=Object_List[i].h and Object_List[i].material==True) or self.h<=0:
                    Object_List[i].Hp-= self.damage
                    self.Del = True
                    Object_List.append(AnimationObject(screen,self.x,self.y,['burst1.png','burst2.png','burst3.png','burst4.png','burst5.png','burst6.png',
                                                                             'burst7.png','burst8.png','burst9.png','burst10.png','burst11.png','burst12.png'],
                                                       0.5, self.h+1, 0, False,False))
                    break
            else:
                if (pygame.sprite.collide_mask(Object_List[i],Object_List[MyIndex])!=None  and i!=MyIndex and self.h<=Object_List[i].h and Object_List[i].material==True) or self.h<=0:
                    Object_List[i].Hp-= self.damage
                    self.Del = True
                    Object_List.append(AnimationObject(screen,self.x,self.y,['burst1.png','burst2.png','burst3.png','burst4.png','burst5.png','burst6.png',
                                                                             'burst7.png','burst8.png','burst9.png','burst10.png','burst11.png','burst12.png'],
                                                       0.5, self.h+1, 0, False,False))
                    break
        self.image = self.Animation_List[ceil(self.animations)]
        self.animations+=self.fps
        if self.animations >= len(self.Animation_List)-1:
            self.animations = 0
        dt = time_passed/1000
        self.Vh -= 9.8*dt
        self.h+=self.Vh*dt
        self.x += (self.Vx-pVx)*dt
        self.y += (self.Vy-pVy)*dt
        self.image = pygame.transform.rotate(self.image, self.grad)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, (self.x, self.y))
        return Object_List
class Block(AnimationObject,Object,Sprite):
    def __init__(self, screen, x, y, Animation_List, h, grad,Hp):
        AnimationObject.__init__(self, screen, x, y, Animation_List, 0, h, grad, True, True)
        self.Hp = Hp
    def update(self, screen, time_passed, pVx, pVy, Object_List, MyIndex):
        if self.Hp<=0:
            self.Del = True
        self.image = pygame.transform.rotate(self.image, self.grad)
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        Object.update(self, screen, time_passed, pVx, pVy)
        return Object_List
