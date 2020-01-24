from main2 import *
import pygame
from pygame.sprite import Sprite
from pygame.locals import *
class Mouse(Sprite):
    def __init__(self,img_filename,pos):
        Sprite.__init__(self)
        self.pos=pos
        self.image = pygame.image.load(img_filename)
        self.rect=self.image.get_rect(center=self.pos)
    def update(self,screen):
        self.pos=pygame.mouse.get_pos()
        self.rect=self.image.get_rect(center=self.pos)
        screen.blit(self.image, self.rect)
class Object(Sprite):
    def __init__(self,img_filename,x,y,index):
        Sprite.__init__(self)
        self.index=index
        self.font=pygame.font.Font(None,36)
        self.x=x
        self.y=y
        self.base_image = pygame.image.load(img_filename)
        self.image = self.base_image
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.select_animation=False
        self.select=False
        self.select_time=0
        self.out_element=[]
    def update(self,screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
        draw_index=self.font.render(str(self.index),1,(0,0,0))
        screen.blit(draw_index,(self.x,self.y))
class Thread_element(Sprite):
    def __init__(self,img_filename,x,y,text):
        self.image=pygame.image.load(img_filename)
        self.x=x
        self.y=y
        self.font=pygame.font.Font(None,16)
        self.text=text
        self.next_element=[]
    def update(self,screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
        draw_text=self.font.render(self.text,1,(0,0,0))
        screen.blit(draw_text,(self.x-30,self.y))
class Connection():
    def __init__(self,element1,element2):
        self.element1=element1
        self.element2=element2
        self.connection=[element1.index,element2.index]
def screen_update(Object_List,mouse):
    for i in Object_List:
        if pygame.sprite.collide_rect(i,mouse)==1:
            i.select_animation=True
            i.image = pygame.image.load('select.png')
            if pygame.mouse.get_pressed(0)[0]==1:
                i.x=mouse.pos[0]
                i.y=mouse.pos[1]
                break
            if pygame.mouse.get_pressed(0)[2]==1 and i.select==False:
                i.select=True
                i.select_time=pygame.time.get_ticks()
                pygame.time.delay(100)
            elif pygame.mouse.get_pressed(0)[2]==1 and i.select==True:
                i.select=False
                pygame.time.delay(100)
        else:
            i.select_animation=False
            i.image = pygame.image.load('element.png')
        if i.select==True:
            i.image=pygame.image.load('element_connect.png')
def new_connections(Object_List):
    for i in range(0,len(Object_List)):
        if Object_List[i].select==True:
            for j in range(i+1,len(Object_List)):
                if Object_List[j].select==True:
                    if Object_List[i].select_time<Object_List[j].select_time:
                        Object_List[i].out_element.append(Object_List[j].index)
                    else:
                        Object_List[j].out_element.append(Object_List[i].index)
                    Object_List[i].select=False
                    Object_List[j].select=False
def draw_connections(screen,Object_List):
    for i in Object_List:
        for j in i.out_element:
            pygame.draw.line(screen,(0,0,0),[i.x,i.y],[Object_List[j-1].x,Object_List[j-1].y],5)
def new_elements(screen,mouse,index):
    List=[]
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        List.append(Object('element.png',mouse.pos[0],mouse.pos[1],index))
        pygame.time.delay(100)
    return List
def make_state(matrix,S,defect_object,Object_List):
    matrix[S-1][defect_object-1]=0
    for i in Object_List[defect_object-1].out_element:
        matrix[S-1][i-1]=0
        if S!=i:
            matrix=make_state(matrix,S,i,Object_List)
    return matrix
def make_state_matrix(Object_List):
    size=len(Object_List)
    matrix=[[1]*size for i in range(size)]
    for i in range(1,size+1):
        matrix=make_state(matrix,i,i,Object_List)
    return matrix
def Graf_State_Interface():
    #параметры
    Object_List=[]
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
    BG_COLOR = 255, 255, 255
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    #инициализация объектов
    mouse=Mouse('white_pixel.png',pygame.mouse.get_pos())
    #главный цикл
    Mainloop = True
    index=1
    while Mainloop:
        keys = pygame.key.get_pressed()
        # Limit frame speed to 100 FPS
        time_passed = clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Mainloop = False
        screen.fill(BG_COLOR)
        #бновление объектов
        mouse.update(screen)
        new_el=new_elements(screen,mouse,index)
        index+=len(new_el)
        Object_List+=new_el
        new_connections(Object_List)
        draw_connections(screen,Object_List)
        screen_update(Object_List,mouse)
        #отображение объектов
        for i in Object_List:
            i.update(screen)
        pygame.display.update()
    pygame.quit()
    return make_state_matrix(Object_List)
def make_check_thread(result):
    y0=100
    Object_List=[]
    Line_List=[]
    Object_List.append(Thread_element('thread.png',500,y0,''))
    key_element=Object_List[0]
    level_key_element=None
    #FIXX
    for i in range(1,len(result[1])):
        x=key_element.x-100*len(result[1][i])/2
        y0+=100
        for unit in result[1][i]:
            Object_List.append(Thread_element('thread.png',x,y0,'Z'+str(unit.Z)+' C='+str(unit.C)))
            Line_List.append(([key_element.x,key_element.y],[x,y0]))
            if unit.Z==result[0][i-1]:
                level_key_element=Object_List[-1]
            x+=100
        key_element=level_key_element
    return (Object_List,Line_List)
def draw_lines(screen,Line_list):
    for Line in Line_list:
        pygame.draw.line(screen,(0,0,0),[Line[0][0],Line[0][1]],[Line[1][0],Line[1][1]],3)
def Thread_screen(result):
    #параметры
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
    BG_COLOR = 255, 255, 255
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    #инициализация объектов
    thread=make_check_thread(result)
    Object_List=thread[0]
    Line_List=thread[1]
    #главный цикл
    Mainloop = True
    while Mainloop:
        # Limit frame speed to 100 FPS
        time_passed = clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Mainloop = False
        screen.fill(BG_COLOR)
        #бновление объектов
        #отображение объектов
        draw_lines(screen,Line_List)
        for i in Object_List:
            i.update(screen)
        pygame.display.update()
    pygame.quit()
