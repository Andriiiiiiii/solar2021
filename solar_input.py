# coding: utf-8
# license: GPLv3
import time

import pygame
import pygame.freetype
import os
from solar_objects import Star, Planet
from solar_vis import DrawableObject


def read_space_objects_data_from_file(input_filename):
    """Считывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """
    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь слеюущий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.

    **star** — объект звезды.
    """
    split = line.split()
    for i in range(1, len(split)):
        try:
            split[i] = float(split[i])
        except ValueError:
            pass
    star.R = split[1]
    star.color = split[2]
    star.m = split[3]
    star.x = split[4]
    star.y = split[5]
    star.Vx = split[6]
    star.Vy = split[7]


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Входная строка должна иметь слеюущий формат:

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Пример строки:

    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.

    **planet** — объект планеты.
    """
    split = line.split()
    for i in range(len(split)):
        try:
            split[i] = float(split[i])
        except ValueError:
            pass
    planet.R = split[1]
    planet.color = split[2]
    planet.m = split[3]
    planet.x = split[4]
    planet.y = split[5]
    planet.Vx = split[6]
    planet.Vy = split[7]


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            out_file.write("{} {} {} {} {} {} {} {}\n".format(obj.obj.type, obj.obj.R, obj.obj.color, obj.obj.m,
                                                              obj.obj.x, obj.obj.y, obj.obj.Vx, obj.obj.Vy))


def ask_for_file_name(configs_dir, surface: pygame.Surface):
    font = pygame.freetype.SysFont("Times New Roman", 15)
    filenames = os.listdir(configs_dir)
    start_x, start_y = surface.get_width()//4, surface.get_height()//4
    x, y = start_x, start_y
    dy = 20
    for filename in filenames:
        if os.path.splitext(filename)[1] != ".txt":
            print(filename)
            filenames.remove(filename)
            continue
        font.render_to(surface, (x, y), filename, (255, 255, 255))
        y += dy
    pygame.display.update()
    print(filenames)
    while not False:
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            print(event.pos)
            i = (event.pos[1] - start_y)//20
            print(i)
            try:
                return filenames[i]
            except IndexError:
                pass
        if pygame.event.get(pygame.QUIT):
            print("haha")
            pygame.quit()
        time.sleep(1.0/60)


if __name__ == "__main__":
    print("This module is not for direct call!")
