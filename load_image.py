import pygame
import os
import sys


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
