import os
import sys
import pygame
from random import choice


WIDTH, HEIGTH = 300, 400
SIZE = WIDTH, HEIGTH
SIZE_ZASTAVKA = 850, 530
TILE = 30
FPS1 = 60
FPS2 = 100

pygame.init()

screen1 = pygame.display.set_mode(SIZE_ZASTAVKA)
clock1 = pygame.time.Clock()
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
    fon_1 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen1.blit(fon_1, (0, 0))
    font = pygame.font.Font(None, 26)
    text_coord = 110
    for elem in intro_text:
        string_rendered = font.render(elem, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen1.blit(string_rendered, intro_rect)
    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            if event_start.type == pygame.KEYDOWN:
                if event_start.key == pygame.K_SPACE:
                    return 1
                if event_start.key == pygame.K_2:
                    return 2
        pygame.display.flip()
        clock1.tick(FPS1)


def start1_screen():
    fon_2 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen1.blit(fon_2, (0, 0))
    button = Button(385, 100, ('purple'), ('grey'))
    button.draw(210, 400, 'Начать игру', screen1)
    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            act = button.mouse_click(210, 400, 'Начать игру', screen1)
            if act == 1:
                return
        pygame.display.flip()
        clock1.tick(FPS1)



class Button:
    def __init__(self, w, h, color1, color2):
        self.w = w
        self.h = h
        self.color1 = color1
        self.color2 = color2
        self.font = pygame.font.Font(None, 85)

    def draw(self, x, y, message, scr):
        text_button = self.font.render(message, True, self.color1)
        pygame.draw.rect(scr, self.color2, (x, y, self.w, self.h))
        scr.blit(text_button, (x + 15, y + 22))

    def mouse_click(self, x, y, message, scr):
        text_but1 = self.font.render(message, True, self.color1)
        text_but2 = self.font.render(message, True, 'green')

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w:
            if y < mouse[1] < y + self.h:
                scr.blit(text_but2, (x + 15, y + 22))
                if click[0] == 1:
                    return 1
        else:
            scr.blit(text_but1, (x + 15, y + 22))


def read_record():
    with open('record.txt') as f:
        return f.readline()


def write_record(r, s):
    rez = max(int(r), s)
    with open('record.txt', 'w') as f:
        f.write(str(rez))

pygame.mixer.music.load("data/fon.mp3")
volume = 0.2
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)
game_tetris = start_screen()


start1_screen()


