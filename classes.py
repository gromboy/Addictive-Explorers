import pygame
from load_image import load_image


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
        self.hp = 3
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
        print(self.coins)

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
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("shop_sprite.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 100000000
        self.rect.y = 100000000

    def update(self):
        if args and self.rect.collidepoint(args[0].pos):
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
        self.rect.x = 508
        self.rect.y = 248
        self.cost = 50

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            hero.dmg += 1
            hero.coins -= self.cost
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        if hero.coins < self.cost:
            text_surface = my_font.render('Недостаточно средств', False, (255, 255, 255))
            screen_shop.blit(text_surface, (0, 0))


class Hpup(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("hpup.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 246
        self.cost = 30

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            hero.hp += 1
            hero.coins -= self.cost
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        if hero.coins < self.cost:
            text_surface = my_font.render('Недостаточно средств', False, (255, 255, 255))
            screen_shop.blit(text_surface, (0, 0))


class ExitShop(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("shop.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 18
        self.rect.y = 16

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            pygame.quit()


class Exit(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("exit.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 18
        self.rect.y = 16

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            save_progress()
            pygame.quit()


class Monster(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("monster.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 100000
        self.rect.y = 1000000

    def update(self):
        if args and self.rect.collidepoint(args[0].pos):
            battle_exist()


class Battle(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("battle.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Damage(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("damage.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 508
        self.rect.y = 248

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            enemy.hp -= hero.dmg
            pygame.font.init()
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'-{hero.dmg} HP', False, (255, 255, 255))
            screen_battle.blit(text_surface, (0, 0))


class Heal(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("heal.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 246

    def update(self, *args):
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        if args and self.rect.collidepoint(args[0].pos):
            if hero.hp_in_battle != hero.hp:
                hero.hp_in_battle += 1
                text_surface = my_font.render('+1 HP', False, (255, 255, 255))
            else:
                text_surface = my_font.render('У вас максимальное здоровье', False, (255, 255, 255))
        screen_battle.blit(text_surface, (0, 0))


class Coin(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("coin.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 1000000
        self.rect.y = 100000

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            hero.coins += 1


class Menu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("menu.png")
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
        self.rect.x = 508
        self.rect.y = 248

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            game_exist()


class Load(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("load.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 246

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            load_progress()


class End(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("end.png")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class MenuBut(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = load_image("load.png")

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 246

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].pos):
            menu_exist()
