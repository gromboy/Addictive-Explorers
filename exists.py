import pygame


def game_exist():
    # Настройки окна и отображения
    global width, height
    running = True  # Флаг для работы программы

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    all_sprites_shop = pygame.sprite.Group()
    all_sprites_battle = pygame.sprite.Group()
    all_sprites_end = pygame.sprite.Group()

    clock = pygame.time.Clock()  # Создание объекта для отслеживания времени

    # Создание спрайтов главного экрана
    hero = Hero(load_image("main_character.png"), 4, 7, 0, 0)
    shop = Shop(all_sprites)
    monster = Monster(all_sprites)
    coin = Coin(all_sprites)
    bg = pygame.sprite.Sprite(all_sprites)  # Фоновый спрайт
    bg.image = load_image('background.png')  # Установка изображения фона
    bg.rect = bg.image.get_rect()

    # Основной игровой цикл
    while running:
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Обработка события выхода из программы
                running = False
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                # Обработка нажатия клавиш для движения героя
                hero.move(event.key)
            if event.type == pygame.KEYUP and event.key in (
                    pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                # Обработка отпускания клавиш и остановки движения героя
                hero.stop_move()
            if spritecollideany(coin, all_sprites):
                hero.coins += 1
                spritecollideany(hero, all_sprites).kill()
            if spritecollideany(shop, all_sprites):
                shop_exist()
            if spritecollideany(monster, all_sprites):
                battle_exist()
                spritecollideany(hero, all_sprites).kill()

        screen.fill('black')  # Заливка экрана черным цветом

        all_sprites.draw(screen)  # Отрисовка всех спрайтов на экране
        all_sprites.update()  # Обновление состояния спрайтов

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение частоты кадров

    pygame.quit()  # Закрытие Pygame\


def menu_exist():

    pygame.display.set_caption('Addictive Explorers')  # Установка заголовка окна
    size = width, height = 800, 450
    screen_menu = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_menu)

    running_menu = True

    while running_menu:
        Menu(all_sprites_menu)
        Exit(all_sprites_menu)
        Load(all_sprites_menu)
        Start(all_sprites_menu)

        screen_menu.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
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

    while running_end:

        End(all_sprites_end)
        Exit(all_sprites_end)
        MenuBut(all_sprites_end)

        screen_end.fill(pygame.Color('black'))

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
    running_shop = True

    size = width, height = 800, 450
    screen_shop = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_shop)

    while running_shop:

        Shop_menu(all_sprites_shop)
        ExitShop(all_sprites_shop)
        Dmgup(all_sprites_shop)
        Hpup(all_sprites_shop)

        screen_shop.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_shop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in all_sprites_shop:
                    sprite.update(event)
            all_sprites_shop.draw(screen_shop)
            pygame.display.flip()
    pygame.quit()


def battle_exist():
    running_battle = True

    size = width, height = 800, 450
    screen_battle = pygame.display.set_mode(size)
    pygame.display.set_icon(screen_battle)

    while running_battle:

        hod = 1
        Battle(all_sprites_battle)
        Damage(all_sprites_battle)
        Heal(all_sprites_battle)

        screen_shop.fill(pygame.Color('black'))

        if hod:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_battle = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in all_sprites_battle:
                        sprite.update(event)
                if enemy.hp <= 0:
                    running_battle = False
                    end_exist()
            hod = 0
        else:
            damage = randint(1,2)
            hero.hp_in_battle -= damage

            pygame.font.init()
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'-{damage} HP', False, (255, 255, 255))
            screen_battle.blit(text_surface, (0, 0))
            hod = 1
        if hero.hp_in_battle <= 0:
            pygame.quit()
            end_exist()
        all_sprites_battle.draw(screen_battle)

        pygame.display.flip()

    pygame.quit()
