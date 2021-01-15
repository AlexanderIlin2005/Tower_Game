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
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            vac = Vaccine(y=self.rect.centery)
            vaccines.add(vac)
        elif args and args[0].type == pygame.KEYDOWN:
            print(args[0].key)
            if args[0].key == 275:
                self.rect.x += 150
            if args[0].key == 276:
                self.rect.x -= 150
            if args[0].key == 274:
                self.rect.y += 150
            if args[0].key == 273:
                self.rect.y -= 150


class Vaccine(pygame.sprite.Sprite):

    def __init__(self, *group, y):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Documents/шприц.png")
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.centery = y

    def update(self, *args):
        self.rect.x += 5
        if self.rect.x > 700:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Desktop/virus2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 10
        self.hp = 3

    def update(self, *args):
        self.rect.x -= 2
        hits = pygame.sprite.spritecollide(self, vaccines, False)
        if hits:
            for hit in hits:
                hit.kill()
                self.hp -= damage
        if self.hp <= 0:
            self.kill()


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра "Доктора против вирусов"')
doctors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
vaccines = pygame.sprite.Group()
damage = 1

for i in range(1):
    doc = Doctor()
    enemy = Enemy()
    doctors.add(doc)
    enemies.add(enemy)
fps = 60
clock = pygame.time.Clock()
running = True
fr_c = 0
rate_of_fire = 50
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        doctors.update(event)
    enemies.update()
    vaccines.update()
    doctors.draw(screen)
    enemies.draw(screen)
    vaccines.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
    fr_c += 1
