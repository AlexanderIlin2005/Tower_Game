import random
import sqlite3

import pygame
import pygame_gui


def load_image(path):
    image = pygame.image.load(path)
    return image


def update_record():
    if exp > record:
        cur.execute(f"""UPDATE players SET record = {exp} WHERE player = '{player}'""")
        con.commit()


def write_exp_and_record(number):
    text = font.render(f"Ваши очки: {number}", True, (0, 0, 255))
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))
    text = font.render(f"Рекорд: {record}", True, (0, 0, 255))
    text_x = 600
    text_y = 10
    screen.blit(text, (text_x, text_y))


def draw_rects():
    for i2 in range(4):
        x = 0
        y = 155 + (120 * i2)
        rect = pygame.Rect(x, y, 1000, 70)
        pygame.draw.rect(screen, (195, 213, 229), rect)


def do_gameover(details):
    global running, clock, fps, playing

    def write_info():
        global exp

        texts = [font.render("Игра окончена", True, (0, 0, 255)), font.render(details, True, (0, 0, 255)),
                 font.render(f"Ваш результат: {exp}", True, (0, 0, 255))]
        text_x = 300
        text_y = 350
        text_rect = pygame.Rect(text_x - 10, text_y - 10, 430, 145)
        frame_rect = pygame.Rect(text_x - 15, text_y - 15, 435, 150)
        pygame.draw.rect(screen, (200, 200, 200), text_rect)
        pygame.draw.rect(screen, (180, 180, 180), frame_rect, 10)
        screen.blit(texts[0], (text_x, text_y))
        text_y += 40
        screen.blit(texts[1], (text_x, text_y))
        text_y += 40
        screen.blit(texts[2], (text_x, text_y))

    def draw_top3():
        max_ = len((max(best_players, key=lambda a: len(a[0])))[0])
        texts = [font.render(f"1){best_players[0][0]}" +
                             f"""{'  ' * (8 + (max_ - len(best_players[0][0])) - 
                                          (2 if '(вы)' in best_players[0][0].lower() else 0))}""" +
                             f"{best_players[0][1]}", True, (0, 0, 255)
                             ),
                 font.render(f"2){best_players[1][0]}" +
                             f"""{'  ' * (8 + (max_ - len(best_players[1][0])) - 
                                          (2 if '(вы)' in best_players[1][0].lower() else 0))}""" +
                             f"{best_players[1][1]}", True, (0, 0, 255)
                             ),
                 font.render(f"3){best_players[2][0]}" +
                             f"""{'  ' * (8 + (max_ - len(best_players[2][0])) - 
                                          (2 if '(вы)' in best_players[2][0].lower() else 0))}""" +
                             f"{best_players[2][1]}", True, (0, 0, 255)
                             ),



                 ]
        text_x = 300
        text_y = 150
        text_rect = pygame.Rect(text_x - 10, text_y - 10, 430, 195)
        frame_rect = pygame.Rect(text_x - 15, text_y - 15, 435, 200)
        pygame.draw.rect(screen, (200, 200, 200), text_rect)
        pygame.draw.rect(screen, (180, 180, 180), frame_rect, 10)
        screen.blit(texts[0], (text_x, text_y))
        text_y += 60
        screen.blit(texts[1], (text_x, text_y))
        text_y += 60
        screen.blit(texts[2], (text_x, text_y))
        line_rect = pygame.Rect(285, 195, 430, 10)
        pygame.draw.rect(screen, (180, 180, 180), line_rect)
        line_rect2 = pygame.Rect(285, 260, 430, 10)
        pygame.draw.rect(screen, (180, 180, 180), line_rect2)
        line_rect3 = pygame.Rect(550, 135, 10, 200)
        pygame.draw.rect(screen, (180, 180, 180), line_rect3)

    manager2 = pygame_gui.UIManager((1000, 600))
    play_rect2 = pygame.Rect((400, 520), (200, 50))
    play2 = pygame_gui.elements.UIButton(
        relative_rect=play_rect2,
        manager=manager2,
        text="Начать заново",
    )
    update_record()
    best_players = [list(i) for i in
                    cur.execute("""SELECT DISTINCT player, record FROM players ORDER BY record DESC""").fetchmany(3)]
    for i in best_players:
        if i[0] == player:
            i[0] = i[0] + "(ВЫ)"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                con.close()
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play2:
                        running = False
            manager2.process_events(event)

        draw_rects()
        enemies.draw(screen)
        doctors.draw(screen)
        smiles.draw(screen)
        vaccines.draw(screen)
        write_exp_and_record(exp)
        write_info()
        draw_top3()
        manager2.update(time_delta=time_delta)
        manager2.draw_ui(screen)
        clock.tick(fps)
        pygame.display.flip()


class Doctor(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("data/doctor500.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 150
        self.move_rate = 120

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            vac = Vaccine(y=self.rect.centery)
            vaccines.add(vac)
        elif args and args[0].type == pygame.KEYDOWN:
            global super_power_exp, paused
            # if args[0].key == 275:
            #    self.rect.x += 150
            # if args[0].key == 276:
            #    self.rect.x -= 150
            print(args[0].key)
            if args[0].key == 1073741905 and self.rect.y + self.move_rate <= 600:  # вверх
                if not paused:
                    self.rect.y += self.move_rate
            if args[0].key == 1073741906 and self.rect.y - self.move_rate >= 145:  # вниз
                if not paused:
                    self.rect.y -= self.move_rate
            if args[0].key == 32:  # пробел
                if not paused:
                    vac = Vaccine(y=self.rect.centery)
                    vaccines.add(vac)
            if args[0].key == 1073742053:  # правый shift
                if super_power_exp >= 1:
                    for enemy in enemies:
                        enemy.kill()
                    super_power_exp = 0
            if args[0].key == 27:
                paused = True
                pygame.mixer.music.pause()
            elif args[0].key != 27:
                paused = False
                pygame.mixer.music.unpause()


class Vaccine(pygame.sprite.Sprite):

    def __init__(self, *group, y):
        super().__init__(*group)
        self.image = load_image("data/shpritz.png")
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.centery = y - 2

    def update(self, *args):
        self.rect.x += 5
        if self.rect.x > 950:
            self.kill()


class Smile(pygame.sprite.Sprite):

    def __init__(self, *group, n):
        super().__init__(*group)
        self.image = load_image(f"data/смайл{random.choice([1, 2, 3])}.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.y = 160 + (120 * n)
        self.hp = 2

    def update(self, *args):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            y = hits[0].rect.y
            self.hp -= 1
            if self.hp == 0:
                for hit in hits:
                    hit.kill()
                self.kill()
            if self.hp == 1:
                self.image = load_image("data/больной смайлик.png")
                for en in enemies:
                    if en.rect.y == y:
                        en.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("data/virus1.png")
        self.images = [load_image("data/virus3.png"), load_image("data/virus5.png")]
        self.rect = self.image.get_rect()
        self.rect.x = 800 + random.randint(-150, 150)
        self.rect.y = 150 + (120 * random.randint(0, 3))
        self.hp = 3

    def update(self, *args):
        global exp, super_power_exp
        self.rect.x -= 2
        hits = pygame.sprite.spritecollide(self, vaccines, False)
        if hits:
            for hit in hits:
                if super_power_exp < 1:
                    super_power_exp += 0.01
                hit.kill()
                self.hp -= damage
                if self.hp == 2:
                    self.image = self.images[0]
                if self.hp == 1:
                    self.image = self.images[1]
        if self.rect.x < 20:
            do_gameover("Вирус пробрался!")
        if self.rect.x < doc.rect.x + doc.rect.width - 30 and self.rect.y == doc.rect.y:
            update_record()
            do_gameover("Доктор заразился!")
        if self.hp <= 0:
            exp += 1
            self.kill()


pygame.mixer.init()
pygame.mixer.music.load("data/Neon_Theme_Music_Mp3.mp3")
pygame.init()
font = pygame.font.Font("data/Phosphate.ttc", 40)
font2 = pygame.font.Font("data/Phosphate.ttc", 20)
font3 = pygame.font.Font("data/Phosphate.ttc", 80)
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Игра "Вакцинация"')
pygame.mixer.music.play(-1)
player = ""
db_name = "data/players.db"
con = sqlite3.connect(db_name)
cur = con.cursor()
record = 0
paused = False
while True:
    super_power_exp = 0
    doctors = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    vaccines = pygame.sprite.Group()
    smiles = pygame.sprite.Group()
    damage = 1
    num_of_enemies = 1
    manager = pygame_gui.UIManager((1000, 600))
    fon = pygame.image.load("data/oblozhka 3.png")
    doc = Doctor()
    doctors.add(doc)
    for i in range(10):
        enemy = Enemy()
        enemies.add(enemy)
    for i in range(4):
        smile = Smile(n=i)
        smiles.add(smile)
    exp = 0
    fps = 60
    clock = pygame.time.Clock()
    running = True
    fr_c = 0
    enemy_rate = 250
    playing = False
    block = False
    show_about_game = False
    play_rect = pygame.Rect((420, 525), (100, 50))
    play = pygame_gui.elements.UIButton(
        relative_rect=play_rect,
        manager=manager,
        text="Играть",
    )
    about_game_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((5, 5), (100, 50)),
        manager=manager,
        text="Обучение",
    )
    play.__setattr__("visible", False)
    player_entry = pygame_gui.elements.UITextEntryLine(
        manager=manager,
        relative_rect=pygame.Rect((400, 270), (140, 50))
    )
    info = pygame_gui.elements.UITextBox(
        manager=manager,
        html_text="Игра «Вакцинация против вирусов»:<br />"
                  "Задача игрока перемещать доктора по дорожкам (вверх/вниз), стреляя"
                  " вакциной из шприца в надвигающиеся вирусы. Пропущенные доктором"
                  "вирусы атакуют смайлы, заражая их. Игрок зарабатывает очки за"
                  " обезвреживание вирусов. Вирус слабеет посла попадания в него вакцины."
                  "После попадания третьей дозы вакцины вирус погибает."
                  "За определенное число попаданий по вирусам"
                  " игрок получает «способность» полностью очистить экран от противника.<br />"
                  "УПРАВЛЕНИЕ:<br />"
                  " - Для стрельбы используйте пробел<br />"
                  " - Для перемещения используйте стрелки вверх/вниз<br />"
                  " - Для использования способности нажмите правый shift<br />"
                  " - Приостановить игру можно нажатием клавиши Escape, для"
                  " продолжения используйте любую клавишу(кроме F1 - F12)<br />"
                            "Победим пандемию вакцинацией!",
        relative_rect=pygame.Rect((50, 50), (550, 310))
    )
    info.__setattr__("visible", False)
    while running:
        screen.fill((255, 255, 255))
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play:
                        playing = True
                        show_about_game = False
                        player = player_entry.text.strip(" ")
                        players = cur.execute(f"""SELECT player FROM players""").fetchall()
                        print(players)
                        players_list = [pl[0] for pl in players]
                        if player in players_list:
                            get = f"SELECT record FROM players WHERE player = '{player}'"
                            record = cur.execute(get).fetchone()[0]
                        else:
                            cur.execute(f"INSERT INTO players(player, record) VALUES('{player}', 0)""")
                        con.commit()
                    if event.ui_element == about_game_btn:
                        if info.visible:
                            info.__setattr__("visible", False)
                        else:
                            info.__setattr__("visible", True)
            if playing:
                doctors.update(event)
            if not playing:
                if player_entry.text.strip(" ") != "":
                    play.__setattr__("visible", True)
                else:
                    play.__setattr__("visible", False)
                manager.process_events(event)
        if not playing:
            screen.blit(fon, (0, -117))
            manager.draw_ui(screen)
            manager.update(time_delta=time_delta)
        if playing:
            if not paused:
                enemies.update()
                vaccines.update()
                smiles.update()
            draw_rects()
            enemies.draw(screen)
            doctors.draw(screen)
            smiles.draw(screen)
            write_exp_and_record(exp)
            vaccines.draw(screen)
            if paused:
                text = font3.render("ПАУЗА", True, (0, 0, 255))
                screen.blit(text, (390, 260))
            if super_power_exp < 1:
                text = font2.render(f"Готовность способности: {int((super_power_exp / 1) * 100)}%", True, (0, 0, 255))
                screen.blit(text, (10, 60))
            else:
                text = font2.render(f"Способность полностью готова(нажмите rshift)", True, (0, 0, 255))
                screen.blit(text, (10, 60))
        clock.tick(fps)
        pygame.display.flip()
        if playing and not paused:
            if fr_c % enemy_rate == 0:
                if num_of_enemies < 3:
                    num_of_enemies += 0.1
                if enemy_rate > 50:
                    enemy_rate -= 10
                for i in range(int(num_of_enemies)):
                    if len(enemies) < 10:
                        en = Enemy()
                        enemies.add(en)
            fr_c += 1
        if not smiles:
            do_gameover("Вирус победил!")
    update_record()
