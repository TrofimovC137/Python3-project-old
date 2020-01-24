import pygame, math

class Sprite:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
    def render(self, screen, pos = (0, 0), angle = 0):
        #Поворачиваю картинку
        print('rot angle =', angle)
        image = pygame.transform.rotate(self.image, angle)
        self.rect = image.get_rect(center=self.rect.center)
        screen.blit(image, self.rect)
    image = 0

pygame.init()
screen = pygame.display.set_mode((800, 600))

sprite = Sprite('Jmato.png')
angle = 0

clok = pygame.time.Clock()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: exit(0)
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: exit(0)

    screen.fill((100, 100, 100))
    sprite.render(screen, (400, 400), angle)
    angle += 1
    pygame.display.update()
    print(angle)
    clok.tick(30)
