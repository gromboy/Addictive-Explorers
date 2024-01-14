import os
import sys

import pygame

pygame.init()

FPS = 10


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


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


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('background.png')
        self.rect = self.image.get_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_on_map)
        self.image = load_image('coin.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.spritecollideany(hero, coins_on_map):
            hero.coins += 1
            self.remove(coins_on_map)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows - 1):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

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

    def move(self, direction):
        self.moving = True
        self.direction = direction
        self.cur_frame = self.directions[direction][2]

    def stop_move(self):
        self.moving = False
        self.cur_frame = self.directions[self.direction][2]
        self.image = self.frames[self.cur_frame]


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


def main():
    # settings
    global all_sprites, width, height, trees, screen, coins_on_map, hero
    size = width, height = 800, 450
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Addictive Explorers')
    running = True
    # settings
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    bg = BackGround()
    hero = Hero(load_image("main_character.png"), 4, 7, 0, 0)
    trees = pygame.sprite.Group()
    coins_on_map = pygame.sprite.Group()
    Tree(load_image('trees.png'), 100, 100, 0, trees)
    Tree(load_image('trees.png'), 300, 100, 1, trees)
    Tree(load_image('trees.png'), 200, 350, 1, trees)
    key_translator = {pygame.K_w: pygame.K_UP,
                      pygame.K_s: pygame.K_DOWN,
                      pygame.K_a: pygame.K_LEFT,
                      pygame.K_d: pygame.K_RIGHT}
    coins = [(200, 100), (200, 200), (400, 350)]
    for x, y in coins:
        Coin(x, y)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
