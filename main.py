from exists import shop_exist, battle_exist, game_exist, menu_exist, end_exist
from load_image import load_image
from classes import (Hero, Shop, Coin, Monster, Shopmenu, Hpup, Dmgup, Exit, Battle, Heal, Damage, Menu, Start,
                     End, Load, MenuBut)
from progress import save_progress, load_progress
import pygame
from pygame.sprite import spritecollideany
load_progress()
size = width, height = 800, 450
screen = pygame.display.set_mode(size)
FPS = 10  # Устанавливаем желаемое количество кадров в секунду


# Основная функция программы
def main():
    menu_exist()


# Запуск основной функции программы, если файл запускается напрямую
if __name__ == '__main__':
    main()
