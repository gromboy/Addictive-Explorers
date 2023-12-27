import os
import sys
import pygame

FPS = 10  # Устанавливаем желаемое количество кадров в секунду

# Функция для загрузки изображений, используется для создания спрайтов


def load_image(name, colorkey=None):
    # Путь к файлу изображения
    fullname = os.path.join('data', name)
    # Проверка наличия файла
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    # Загрузка изображения в pygame
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # Если указан параметр colorkey, настраиваем прозрачность
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        # Иначе используем альфа-канал для прозрачности
        image = image.convert_alpha()
    return image

# Класс героя, который наследуется от pygame.sprite.Sprite
class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)  # Инициализация спрайта
        self.frames = []  # Список кадров анимации героя
        self.cut_sheet(sheet, columns, rows)  # Вырезаем кадры из спрайта
        self.cur_frame = 1  # Текущий кадр анимации
        self.image = self.frames[self.cur_frame]  # Устанавливаем изображение для текущего кадра
        self.rect = self.rect.move(x, y)  # Устанавливаем положение героя на экране
        self.moving = False  # Флаг для движения героя
        # Скорость перемещения
        self.pix = 9
        # Направления движения и их соответствующие клавиши
        self.directions = {pygame.K_DOWN: (0, self.pix, 0),
                           pygame.K_UP: (0, -self.pix, 1),
                           pygame.K_LEFT: (-self.pix, 0, 2),
                           pygame.K_RIGHT: (self.pix, 0, 3)}
        self.direction = pygame.K_UP  # Начальное направление - вверх

    # Метод для вырезания кадров из спрайта
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows - 1):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                # Вырезаем кадр из спрайта и добавляем в список кадров анимации
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # Метод обновления состояния героя
    def update(self):
        if self.moving:
            # Анимация движения героя
            self.cur_frame = (self.cur_frame + 4) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            # Вычисляем новое положение героя при движении
            to_move = self.rect.move(*self.directions[self.direction][0:2])
            x, y = to_move.x, to_move.y
            # Проверка на выход за границы экрана
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
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)  # Инициализация спрайта
        self.image = load_image('shop.png')  # Устанавливаем изображение
        self.rect = self.rect.move(x, y)  # Устанавливаем положение магазина на экране
    def move(self, x, y):
        self.moving = True


# Основная функция программы
def main():
    # Настройки окна и отображения
    global all_sprites, width, height
    size = width, height = 800, 450
    screen = pygame.display.set_mode(size)  # Создание окна
    pygame.display.set_caption('Addictive Explorers')  # Установка заголовка окна
    running = True  # Флаг для работы программы

    # Создание группы спрайтов
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()  # Создание объекта для отслеживания времени
    #bg = pygame.sprite.Sprite(all_sprites)  # Фоновый спрайт
    # Создание экземпляра героя
    hero = Hero(load_image("main_character.png"), 4, 7, 0, 0)
    shop = Shop()
    #bg.image = load_image('background.png')  # Установка изображения фона
    #bg.rect = bg.image.get_rect()

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

        screen.fill('black')  # Заливка экрана черным цветом
        all_sprites.draw(screen)  # Отрисовка всех спрайтов на экране
        all_sprites.update()  # Обновление состояния спрайтов
        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение частоты кадров

    pygame.quit()  # Закрытие Pygame

# Запуск основной функции программы, если файл запускается напрямую
if __name__ == '__main__':
    main()
