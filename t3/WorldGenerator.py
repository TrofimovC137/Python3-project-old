from Object import *

def HSort(Object_List):
    i=0
    while i<=(len(Object_List)-2):
        if Object_List[i].h > Object_List[i+1].h:
            tmp = Object_List[i+1]
            Object_List[i+1] = Object_List[i]
            Object_List[i] = tmp
            i=0
        else:
            i+=1
    return Object_List
    
def PlayerIndex(Object_List):
    i=0
    index = 0
    while i<=(len(Object_List)-1):
        if Object_List[i].player ==True:
            index = i
            i+=1
        else:
            i+=1
    return index
def ObjectGenerator(screen):
    Object_List=[]
    x, y = 0, 0
    while y<=4:
        while x<=4:
            Object_List.append(AnimationObject(screen, x*100, y*100,['trav.png'],0, 0,0,True,True))
            x+=1
        x = 0
        y+=1
    Object_List.append(Block(screen, 700, 384,['wall.png'],1,0,50))
    Turret_List = [Turret(screen,100,512,50,'MS-1turret.png',2,10,100)]
    Object_List.append(Player(screen, 100, 512, 384, 0, 0, 'MS-1.png', 300, 1, 10, Turret_List,[-1,90]))
    return Object_List
def DelObject(Object_List):
    i=0
    while i<=(len(Object_List)-1):
        if Object_List[i].Del==True:
           del Object_List[i]
           i-=1
        else:
            i+=1
    return Object_List
                               
