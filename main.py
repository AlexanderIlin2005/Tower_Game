import pygame


def load_image(path):
    image = pygame.image.load(path)
    return image


class Doctor(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Downloads/doctor.png")
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self, *args):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Desktop/virus2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 10

    def update(self, *args):
        self.rect.x -= 2


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра "Доктора против вирусов"')
doctors = pygame.sprite.Group()
enemies = pygame.sprite.Group()

for i in range(1):
    doc = Doctor()
    enemy = Enemy()
    doctors.add(doc)
    enemies.add(enemy)
fps = 60
clock = pygame.time.Clock()
running = True
fr_c = 0

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    doctors.update()
    enemies.update()
    doctors.draw(screen)
    enemies.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
    fr_c += 1
