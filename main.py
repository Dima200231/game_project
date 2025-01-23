import os
import sys
import pygame
from random import choice


WIDTH, HEIGTH = 300, 400  # размер игрового поля
SIZE = WIDTH, HEIGTH
SIZE_FON = 850, 530
TILE = 30
FPS = 60
FPS_1 = 100

pygame.init()

screen_0 = pygame.display.set_mode(SIZE_FON)
clock_0 = pygame.time.Clock()
pygame.display.set_caption("The Last race")


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["УПРАВЛЕНИЕ", "",
                  "'A' - движение влево", "'D' - движение вправо", "",
                  '"Гоньщики не гонят.', "",
                  'Гоньщики гоняют, но не загоняются".', "",
                  '           ...цитата из фильма"Суперфорсаж!"', "",
                  "", ""
                  "Нажмите 'Пробел', чтобы продолжить"]
    fon_0 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen_0.blit(fon_0, (0, 0))
    font = pygame.font.Font(None, 26)
    text_coord = 110
    for elem in intro_text:
        string_rendered = font.render(elem, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen_0.blit(string_rendered, intro_rect)
    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            if event_start.type == pygame.KEYDOWN:
                if event_start.key == pygame.K_SPACE:
                    return 1
                if event_start.key == pygame.K_2:
                    return 2  # далее
        pygame.display.flip()
        clock_0.tick(FPS)


# страница с правилами
def start1_screen():
    fon_2 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen_0.blit(fon_2, (0, 0))
    button = Button(385, 100, ('purple'), ('grey'))
    button.draw(210, 400, 'Начать игру', screen_0)
    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            act = button.mouse_click(210, 400, 'Начать игру', screen_0)
            if act == 1:
                return  # начинаем игру
        pygame.display.flip()
        clock_0.tick(FPS)


def game_over(t):
    clock_1 = pygame.time.Clock()
    for c in range(WIDTH):
        for line in range(HEIGTH):
            x = c * TILE + 518
            y = line * TILE + 6
            pygame.draw.rect(screen, choice(colors), (x, y, TILE, TILE), 0)
            pygame.display.flip()
            clock_1.tick(FPS_1)

    for line in range(HEIGTH):
        for c in range(WIDTH):
            x = c * TILE + 518
            y = line * TILE + 6
            pygame.draw.rect(screen, (7, 171, 206), (x, y, TILE - 4, TILE - 4), 0)
            pygame.display.flip()
            clock_1.tick(FPS_1)
    font_3 = pygame.font.Font(None, 45)
    text_end = font_3.render(t, True, (159, 47, 1))
    screen.blit(text_end, (528, 250))
    zx = 518
    step_zx = 1
    line = HEIGTH
    zy = 580
    while True:
        for c in range(WIDTH):
            x = c * TILE + 518
            y = (line - 1) * TILE + 6
            pygame.draw.rect(screen, (7, 171, 206), (x, y, TILE - 4, TILE - 4), 0)

        font = pygame.font.Font(None, 25)
        text_next_over = font.render('ПРОБЕЛ!', True, (159, 47, 1))
        w, h = text_next_over.get_size()
        screen.blit(text_next_over, (zx, zy))
        zx += step_zx
        if zx + w > 819 or zx < 518:
            step_zx = - step_zx
            line -= 3
            zy -= 90
            if line < 0:
                line = HEIGTH

        for event_go in pygame.event.get():
            if event_go.type == pygame.QUIT:
                terminate()
            if event_go.type == pygame.KEYDOWN:
                if event_go.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock_1.tick(FPS)


class Button:
    def __init__(self, wdt, hgt, i_color, a_color):
        self.wdt = wdt
        self.hgt = hgt
        self.i_color = i_color
        self.a_color = a_color
        self.font = pygame.font.Font(None, 85)

    def draw(self, x, y, message, scr):
        text_button = self.font.render(message, True, self.i_color)
        pygame.draw.rect(scr, self.a_color, (x, y, self.wdt, self.hgt))
        scr.blit(text_button, (x + 15, y + 22))

    def mouse_click(self, x, y, message, scr):
        text_button_1 = self.font.render(message, True, self.i_color)
        text_button_2 = self.font.render(message, True, 'green')

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.wdt:
            if y < mouse[1] < y + self.hgt:
                scr.blit(text_button_2, (x + 15, y + 22))
                if click[0] == 1:
                    return 1
        else:
            scr.blit(text_button_1, (x + 15, y + 22))


class Board:
    # создание поля
    def __init__(self, wdt, hgt):
        self.wdt = wdt
        self.hgt = hgt
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = TILE
        self.color_board = (100, 100, 100)
        # запоминаем карту игрового поля и счет
        self.board_map = [[0 for _ in range(WIDTH)] for _ in range(HEIGTH)]
        self.score = 0

    # заносим в карту игрового поля цвет квадрата
    def set_value(self, y_pos, x_pos, c):
        self.board_map[y_pos][x_pos] = c

    # удаление линий, за каждую удаленную линию +100
    def del_line(self):
        line = HEIGTH - 1  # посл линия
        for row in range(HEIGTH - 1, -1, -1):
            k = 0  # счетчик заполненных клеток
            for i_1 in range(WIDTH):
                if self.board_map[row][i_1]:
                    k += 1
                self.board_map[line][i_1] = self.board_map[row][i_1]
            if k < WIDTH:
                line -= 1
            else:
                self.score += 100

    # отрисовка клеток
    def render(self, scr):
        for y in range(self.hgt):
            for x in range(self.wdt):
                pygame.draw.rect(scr, self.color_board, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


# функция возвращает число - рекордный счет, записанный в файле
def read_record():
    with open('record.txt') as f:
        return f.readline()


# перезаписываем рекорд, если счет больше
def write_record(r, s):
    rez = max(int(r), s)
    with open('record.txt', 'w') as f:
        f.write(str(rez))

pygame.mixer.music.load("data/fon.mp3")
volume = 0.2
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)
# стартовая страница с историей и выбором количества фигур
game_tetris = start_screen()


# страница с правил1ами
start1_screen()

# фоновая музыка

