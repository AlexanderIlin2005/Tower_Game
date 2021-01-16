import random

import pygame


def load_image(path):
    image = pygame.image.load(path)
    return image


def write_exp_and_record(number):
    font = pygame.font.Font(None, 40)
    text = font.render(f"Ваши очки: {number}", True, (255, 0, 0))
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))


def draw_rects():
    for i2 in range(4):
        x = 0
        y = 155 + (120 * i2)
        rect = pygame.Rect(x, y, 1000, 70)
        pygame.draw.rect(screen, (240, 240, 240), rect)


def draw_rect(x, y, hp):
    rect = pygame.Rect(x + 2, y, 16 * hp, 3)
    pygame.draw.rect(screen, (255, 0, 0), rect)


class Doctor(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Downloads/doctor500.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 145
        self.move_rate = 120

    def update(self, *args):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            self.kill()
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            vac = Vaccine(y=self.rect.centery)
            vaccines.add(vac)
        elif args and args[0].type == pygame.KEYDOWN:
            # print(args[0].key)
            # if args[0].key == 275:
            #    self.rect.x += 150
            # if args[0].key == 276:
            #    self.rect.x -= 150
            if args[0].key == 274 and self.rect.y + self.move_rate <= 600:
                self.rect.y += self.move_rate
            if args[0].key == 273 and self.rect.y - self.move_rate >= 145:
                self.rect.y -= self.move_rate
            if args[0].key == 32:
                vac = Vaccine(y=self.rect.centery)
                vaccines.add(vac)


class Vaccine(pygame.sprite.Sprite):

    def __init__(self, *group, y):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Documents/шприц.png")
        self.rect = self.image.get_rect()
        self.rect.x = 270
        self.rect.centery = y - 5

    def update(self, *args):
        self.rect.x += 5
        if self.rect.x > 950:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("/Users/alexeyilyin/Desktop/virus2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 165 + (120 * random.randint(0, 3))
        self.hp = 3

    def update(self, *args):
        self.rect.x -= 2
        hits = pygame.sprite.spritecollide(self, vaccines, False)
        if hits:
            for hit in hits:
                hit.kill()
                self.hp -= damage
        if self.hp <= 0:
            global exp
            exp += 1
            self.kill()


pygame.init()
size = width, height = 1000, 600
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
enemy_rate = 250
exp = 0
with open("record.txt", "w") as f:
    f.write(f"{exp}")
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        doctors.update(event)
    enemies.update()
    vaccines.update()
    draw_rects()
    for enemy in enemies:
        draw_rect(enemy.rect.x, enemy.rect.y, enemy.hp)
    doctors.draw(screen)
    enemies.draw(screen)
    write_exp_and_record(exp)
    vaccines.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
    if fr_c % enemy_rate == 0:
        en = Enemy()
        enemies.add(en)
    fr_c += 1
