from random import randint

import pygame
from load_image import load_image

FPS = 25


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Hero(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y)
        self.moving = False
        # speed
        self.pix = 9
        self.directions = {pygame.K_DOWN: (0, self.pix, 0),
                           pygame.K_UP: (0, -self.pix, 1),
                           pygame.K_LEFT: (-self.pix, 0, 2),
                           pygame.K_RIGHT: (self.pix, 0, 3)}
        self.direction = pygame.K_UP
        self.new_rect = pygame.sprite.Sprite(all_sprites)
        self.new_rect.image = pygame.Surface((47, 47), pygame.SRCALPHA, 32)
        self.new_rect.rect = pygame.Rect(x, y, 47, 47)
        self.new_rect.mask = pygame.mask.from_surface(self.new_rect.image)
        self.coins = 0
        self.hp = 5
        self.regeneration = 1
        self.hp_in_battle = self.hp
        self.dmg = 1

    # Метод для вырезания кадров из спрайта
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows - 1):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # Метод обновления состояния героя
    def update(self):
        if self.moving:
            self.cur_frame = (self.cur_frame + 4) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            to_move = self.rect.move(*self.directions[self.direction][0:2])
            x, y = to_move.x, to_move.y
            self.new_rect.rect = pygame.Rect(x, y, 47, 47)
            for i in trees:
                if pygame.sprite.collide_rect(self.new_rect, i):
                    return
            if x < 0 or y < 0 or x > width - 47 or y > height - 47:
                return
            self.rect = to_move

    # Метод для начала движения героя в определенном направлении
    def move(self, direction):
        self.moving = True
        self.direction = direction
        self.cur_frame = self.directions[direction][2]

    # Метод для остановки движения героя
    def stop_move(self):
        self.moving = False
        self.cur_frame = self.directions[self.direction][2]
        self.image = self.frames[self.cur_frame]


class Shop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.image = load_image("shop_sprite.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 730
        self.rect.y = 10

    def update(self):
        if pygame.sprite.collide_rect(self, hero):
            hero.rect.x = self.rect.x - 66
            hero.rect.y = self.rect.y
            hero.stop_move()
            shop_exist()


class Shopmenu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("shop.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Dmgup(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("dmgup.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 504
        self.rect.y = 246
        self.cost = 40

    def click(self):
        if hero.coins < self.cost:
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render('Недостаточно средств', False, (255, 0, 0))
            texts_shop.append(text_surface)
        else:
            hero.dmg += 1
            hero.coins -= self.cost
            texts_shop.clear()


class Hpup(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("hpup.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 198
        self.rect.y = 245
        self.cost = 30

    def click(self):
        if hero.coins < self.cost:
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render('Недостаточно средств', False, (255, 0, 0))
            texts_shop.append(text_surface)
        else:
            hero.regeneration += 1
            hero.coins -= self.cost
            texts_shop.clear()


class ExitShop(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("close_shop.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 18
        self.rect.y = 16


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("monster.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(enemies)

    def update(self):
        if pygame.sprite.collide_rect(self, hero):
            self.kill()
            battle_exist()


class NextLevel(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("battle.png")

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Battle(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("battle.png")

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Damage(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("damage.png")
        self.rect = self.image.get_rect()
        self.rect.x = 413
        self.rect.y = 305


class Heal(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("heal.png")

        self.rect = self.image.get_rect()
        self.rect.x = 37
        self.rect.y = 305


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("coin.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(coins_on_map)

    def update(self):
        if pygame.sprite.collide_rect(self, hero):
            hero.coins += 20
            self.kill()


class Menu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("load.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Start(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("start.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 220

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            game_exist()


class Load(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("loadbut.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 350

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            load_progress()


class End(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("endscreen.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class MenuBut(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("endmenu.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 260
        self.rect.y = 253

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            menu_exist()


class Tree(AnimatedSprite):
    def __init__(self, sheet, x, y, type, group):
        super().__init__(sheet, 1, 2, x, y)
        self.type = type
        self.add(group)
        if self.type == 0:
            self.change_type(0)
        elif self.type == 1:
            self.change_type(1)
        else:
            raise ValueError

    def change_type(self, typ):
        self.type = typ
        self.cur_frame = self.type
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)


def game_exist():
    # Настройки окна и отображения
    global width, height, all_sprites, screen, all_sprites_shop, all_sprites_battle, all_sprites_end, trees
    global coins_on_map, hero, enemies
    running = True  # Флаг для работы программы

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    all_sprites_shop = pygame.sprite.Group()
    all_sprites_battle = pygame.sprite.Group()
    all_sprites_end = pygame.sprite.Group()
    coins_on_map = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    size = width, height = 800, 450
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()  # Создание объекта для отслеживания времени

    # Создание спрайтов главного экрана
    trees = pygame.sprite.Group()
    bg = pygame.sprite.Sprite(all_sprites)  # Фоновый спрайт
    bg.image = load_image('background.png')  # Установка изображения фона
    shop = Shop()
    bg.rect = bg.image.get_rect()
    key_translator = {pygame.K_w: pygame.K_UP,
                      pygame.K_s: pygame.K_DOWN,
                      pygame.K_a: pygame.K_LEFT,
                      pygame.K_d: pygame.K_RIGHT}
    coins_on_map = pygame.sprite.Group()
    Coin(50, 30)
    Coin(150, 30)
    Monster(300, 300)
    hero = Hero(load_image("main_character.png"), 4, 7, 0, 0)
    Tree(load_image('trees.png'), 100, 100, 0, trees)
    Tree(load_image('trees.png'), 300, 100, 1, trees)
    Tree(load_image('trees.png'), 200, 350, 1, trees)
    # Основной игровой цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s,
                    pygame.K_d):
                try:
                    hero.move(key_translator[event.key])
                except KeyError:
                    hero.move(event.key)
            if event.type == pygame.KEYUP and event.key in (
                    pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s,
                    pygame.K_d):
                hero.stop_move()
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        coins_on_map.draw(screen)
        coins_on_map.update()
        enemies.draw(screen)
        enemies.update()
        # texts
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        money = my_font.render(f'Money: {hero.coins}', False, (0, 0, 0))
        screen.blit(money, (10, 380))
        # texts
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def menu_exist():
    pygame.display.set_caption('Addictive Explorers')  # Установка заголовка окна
    size = width, height = 800, 450
    screen_menu = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_menu)
    all_sprites_menu = pygame.sprite.Group()
    running_menu = True

    while running_menu:
        Menu(all_sprites_menu)
        Load(all_sprites_menu)
        Start(all_sprites_menu)

        screen_menu.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites_menu:
                    sprite.update(event)
            all_sprites_menu.draw(screen_menu)
            pygame.display.flip()
    pygame.quit()


def end_exist():
    running_end = True

    size = width, height = 800, 450
    screen_end = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_end)
    End(all_sprites_end)
    MenuBut(all_sprites_end)

    while running_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_end = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites_end:
                    sprite.update(event)
        all_sprites_end.draw(screen_end)
        pygame.display.flip()
    pygame.quit()


def shop_exist():
    global screen_shop, running_shop, texts_shop
    running_shop = True
    pygame.font.init()
    size = width, height = 800, 450
    screen_shop = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_shop)
    shop_font = pygame.font.SysFont('Comic Sans MS', 50)
    texts_shop = []
    while running_shop:
        Shopmenu(all_sprites_shop)
        ExitShop(all_sprites_shop)
        dmgup = Dmgup(all_sprites_shop)
        hpup = Hpup(all_sprites_shop)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites_shop:
                    if isinstance(sprite, ExitShop) and sprite.rect.collidepoint(event.pos):
                        running_shop = False
                    if isinstance(sprite, Hpup) and sprite.rect.collidepoint(event.pos):
                        hpup.click()
                        break
                    if isinstance(sprite, Dmgup) and sprite.rect.collidepoint(event.pos):
                        dmgup.click()
                        break
        all_sprites_shop.draw(screen_shop)
        for text in texts_shop:
            screen_shop.blit(text, (100, 0))
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        hp = my_font.render(f'HP: {hero.hp}', False, (255, 0, 0))
        dmg = my_font.render(f'DMG: {hero.dmg}', False, (255, 0, 0))
        money = my_font.render(f'Money: {hero.coins}', False, (255, 0, 0))
        cost_hpup = shop_font.render(str(hpup.cost), False, 'yellow')
        cost_dmgup = shop_font.render(str(dmgup.cost), False, 'yellow')
        screen_shop.blit(money, (10, 300))
        screen_shop.blit(hp, (10, 400))
        screen_shop.blit(dmg, (100, 400))
        screen_shop.blit(cost_hpup, (320, 350))
        screen_shop.blit(cost_dmgup, (620, 350))
        pygame.display.flip()


def battle_exist():
    hero.stop_move()
    global screen_battle, enemy_hp
    running_battle = True
    size = width, height = 800, 450
    screen_battle = pygame.display.set_mode(size)
    pygame.display.set_caption("Battle Window")
    pygame.display.set_icon(pygame.Surface((32, 32)))

    enemy_hp = 5
    hero.hp_in_battle = hero.hp

    Battle(all_sprites_battle)
    Damage(all_sprites_battle)
    Heal(all_sprites_battle)
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    hod = 1
    dmg_text = my_font.render('', False, (255, 255, 255))
    text_surface = my_font.render('', False, (255, 255, 255))
    damage_from_enemy = my_font.render('', False, (255, 255, 255))
    while running_battle:
        if hod:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in all_sprites_battle:
                        if isinstance(sprite, Heal) and sprite.rect.collidepoint(event.pos):
                            if hero.hp_in_battle != hero.hp:
                                hero.hp_in_battle += hero.regeneration
                                hod = 0
                                text_surface = my_font.render('+1 HP', False, (0, 255, 0))
                            else:
                                text_surface = my_font.render('У вас максимальное здоровье', False, (255, 0, 0))
                            break
                        if isinstance(sprite, Damage) and sprite.rect.collidepoint(event.pos):
                            hod = 0
                            enemy_hp -= hero.dmg
                            dmg_text = my_font.render(f'-{hero.dmg} HP', False, (255, 0, 0))
                            break
                    if enemy_hp <= 0:
                        running_battle = False
                        hero.coins += 50
        else:
            damage = randint(1, 2)
            hero.hp_in_battle -= damage
            damage_from_enemy = my_font.render(f'-{damage} HP', False, (255, 0, 0))

            hod = 1

        if hero.hp_in_battle <= 0:
            running_battle = False
            end_exist()

        hp_hero = my_font.render(f'HP: {hero.hp_in_battle}', False, (255, 255, 255))
        hp_enemy = my_font.render(f'HP: {enemy_hp}', False, (255, 255, 255))
        all_sprites_battle.draw(screen_battle)
        screen_battle.blit(text_surface, (10, 5))
        screen_battle.blit(hp_hero, (37, 200))
        screen_battle.blit(hp_enemy, (400, 200))
        screen_battle.blit(damage_from_enemy, (50, 250))
        screen_battle.blit(dmg_text, (450, 250))
        pygame.display.flip()
