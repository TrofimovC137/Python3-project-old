from WorldGenerator import *

def run_game():
    #игровые параметры
   
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
    BG_COLOR = 200, 200, 200
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    #инициализация объектов
    Object_List = ObjectGenerator(screen)

    #главный игровой цикл
    Mainloop = True
    while Mainloop:

        # Limit frame speed to 50 FPS
        time_passed = clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Mainloop = False
        screen.fill(BG_COLOR)

        #удаление объектов
        Object_List=DelObject(Object_List)
        Object_List=HSort(Object_List)
        index = PlayerIndex(Object_List)
        #отображение объектов
        i=0
        while i<=(len(Object_List)-1):
            Object_List=Object_List[i].update(screen,time_passed,Object_List[index].Vx,Object_List[index].Vy,Object_List,i)
            i+=1

       
        #print(len(Object_List))
        pygame.display.update()
    pygame.quit()
    
#программа
run_game()
