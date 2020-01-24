'''010011
101001
010101
001011
100101
111110'''



import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from math import *
from random import randint
class Object(Sprite):
    def __init__(self, screen,img_filename,x,y):
        Sprite.__init__(self)
        self.x=x
        self.y=y
        self.base_image = pygame.image.load(img_filename)
        self.image = self.base_image
        self.screen = screen
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update(self,screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
def tabl_sort(tabl):
    for i in range(0,len(tabl)):
        tabl[i]=tabl[i][i:len(tabl[i])]
    return tabl
def Object_List_init(screen,tabl):
    Object_List=[]
    a=0
    da=360/len(tabl)
    for i in range(0,len(tabl)):
        Object_List.append(Object(screen,'redball.png',300+150*cos(a/57),300+150*sin(a/57)))
        a+=da
    return Object_List
def Line_init(screen,tabl,Object_List):
    Line_List=[]
    Line_Object_List=[]
    for i in range(0,len(tabl)):
        for j in range(0,len(tabl[i])):
            if (tabl[i][j]=='1'):
                Line_List.append([[Object_List[i].x,Object_List[i].y],[Object_List[j].x,Object_List[j].y]])
    for i in range(0,len(Line_List)):
        if (Line_List[i][1][0]-Line_List[i][0][0]>Line_List[i][1][1]-Line_List[i][0][1]):
            for x in range(int(Line_List[i][0][0]),int(Line_List[i][1][0])):
                y=(((x-Line_List[i][0][0])*(Line_List[i][1][1]-Line_List[i][0][1]))/(Line_List[i][1][0]-Line_List[i][0][0])+Line_List[i][0][1])
                Line_Object_List.append(Object(screen,'pixel.png',x,y))
        else:
            for y in range(int(Line_List[i][0][1]),int(Line_List[i][1][1])):
                x=(((y-Line_List[i][0][1])*(Line_List[i][1][0]-Line_List[i][0][0]))/(Line_List[i][1][1]-Line_List[i][0][1])+Line_List[i][0][0])
                Line_Object_List.append(Object(screen,'pixel.png',x,y))
    return Line_Object_List
def Gamilton(screen,Object_List):
    Line_List=[]
    Line_Object_List=[]
    vertex=[]
    for i in range(1,len(Object_List)):
        vertex.append(i)
    old_vertex=0
    while len(vertex)!=0:
        index=randint(0,len(vertex)-1)
        new_vertex=vertex[index]
        del vertex[index]
        Line_List.append([[Object_List[old_vertex].x,Object_List[old_vertex].y],[Object_List[new_vertex].x,Object_List[new_vertex].y]])
        Line_List.append([[Object_List[new_vertex].x,Object_List[new_vertex].y],[Object_List[old_vertex].x,Object_List[old_vertex].y]])
        old_vertex=new_vertex
    Line_List.append([[Object_List[old_vertex].x,Object_List[old_vertex].y],[Object_List[0].x,Object_List[0].y]])
    Line_List.append([[Object_List[0].x,Object_List[0].y],[Object_List[old_vertex].x,Object_List[old_vertex].y]])
    for i in range(0,len(Line_List)):
        if (Line_List[i][1][0]-Line_List[i][0][0]>Line_List[i][1][1]-Line_List[i][0][1]):
            for x in range(int(Line_List[i][0][0]),int(Line_List[i][1][0])):
                y=(((x-Line_List[i][0][0])*(Line_List[i][1][1]-Line_List[i][0][1]))/(Line_List[i][1][0]-Line_List[i][0][0])+Line_List[i][0][1])
                Line_Object_List.append(Object(screen,'pixel.png',x,y))
        else:
            for y in range(int(Line_List[i][0][1]),int(Line_List[i][1][1])):
                x=(((y-Line_List[i][0][1])*(Line_List[i][1][0]-Line_List[i][0][0]))/(Line_List[i][1][1]-Line_List[i][0][1])+Line_List[i][0][0])
                Line_Object_List.append(Object(screen,'pixel.png',x,y))
    return Line_Object_List
def show(screen,Object_List,Line_List):
    for i in range(0,len(Line_List)):
        Line_List[i].update(screen)
    for i in range(0,len(Object_List)):
        Object_List[i].update(screen)
def run():
    print('введите команду 1-построение графа, 2-гамильтонов цикл')
    comand=int(input())
    print('введите количество вершин')
    number_of_center=int(input())
    if comand==1:
        tabl=[0]*number_of_center
        for i in range(0,number_of_center):
            tabl[i]=str(input())
    else:
        tabl=[0]*number_of_center
        for i in range(0,number_of_center):
            tabl[i]='0'*number_of_center
    #tabl=tabl_sort(tabl)
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    BG_COLOR = 200, 200, 200
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    #инициализация объектов
    Object_List=Object_List_init(screen,tabl)
    if comand==1:
        Line_List=Line_init(screen,tabl,Object_List)
    else:
        Line_List=Gamilton(screen,Object_List)
    Mainloop = True
    while Mainloop:
        # Limit frame speed to 10 FPS
        time_passed = clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Mainloop = False
        screen.fill(BG_COLOR)
        #отображение объектов
        show(screen,Object_List,Line_List)
        pygame.display.update()
    pygame.quit()
#программа
run()
