import random
import pygame
import os
import sys


pygame.init()
SIZE_ZASTAVKA = 850, 530
screen1 = pygame.display.set_mode(SIZE_ZASTAVKA)
clock1 = pygame.time.Clock()
pygame.display.set_caption("The Last race")
FPS1 = 60

def load_image(name, size, angle, colorkey=None):
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
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["THE LAST RACE", "",
                  '"Гоньщики не гонят.', "",
                  'Гоньщики гоняют, но не загоняются".', "",
                  '           ...цитата из фильма"Суперфорсаж!"', "",
                  "", ""
                  "Нажмите 'Пробел', чтобы продолжить"]
    fon_1 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen1.blit(fon_1, (0, 0))
    font = pygame.font.Font(None, 34)
    text_coord = 40
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
                    return
            if event_start.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock1.tick(FPS1)

def start1_screen():
    intro_text = ["УПРАВЛЕНИЕ", "",
                  "'A' - движение влево", "'D' - движение вправо", "",
                  "'1' - вкл/выкл музыки", "",
                  "'2' - уменьшение громкости", "",
                  "'3' - увеличение громкости", ""]
    fon_2 = pygame.image.load('data/photo_zastavka.jpg').convert()
    screen1.blit(fon_2, (0, 0))
    button = Button(385, 100, ('purple'), ('grey'))
    button.draw(210, 400, 'Начать игру', screen1)
    font = pygame.font.Font(None, 40)
    text_coord = 20
    for elem in intro_text:
        string_rendered = font.render(elem, True, pygame.Color('red'))
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

pygame.mixer.music.load("sounds/fon.mp3")
volume = 0.2
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

game_racing = start_screen()

start1_screen()

screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('The Last race')
background_color = (0, 0, 0)

my_car_sound = pygame.mixer.Sound('sounds/engine.wav')
my_car_sound.play(-1)

crash_sound = pygame.mixer.Sound('sounds/crash.wav')

font = pygame.freetype.Font(None, 20)

road_group = pygame.sprite.Group()
spawn_road_time = pygame.USEREVENT
pygame.time.set_timer(spawn_road_time, 1000)

cars_group = pygame.sprite.Group()
spawn_time = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_time, 1000)

my_car_image = load_image('my_car.png', (100, 70), 90)
road_image = pygame.image.load('data/road.png')
road_image = pygame.transform.scale(road_image, (500, 800))

car_images = []
car1 = load_image('enemy_car1.png', (100, 70), -90)
car2 = load_image('enemy_car2.png', (110, 70), 90)
car3 = load_image('enemy_car3.png', (100, 70), 90)
car_images.extend((car1, car2, car3))

class MyCar:
    def __init__(self, position, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.game_status = 'game'

    def border(self):
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 0:
            self.rect.left = 0

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 5
        elif key[pygame.K_d]:
            self.rect.x += 5
        self.border()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def crash(self, sound, traffic_cars):
        for car in traffic_cars:
            if car.rect.colliderect(self.rect):
                print('Game over')
                sound.play()
                self.game_status = 'game_over'


class Road(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.y += 3


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def remove(self):
        if self.rect.top > 800:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.remove()

start_time = pygame.time.get_ticks()

road = Road(road_image, (250, 400))
road_group.add(road)
road = Road(road_image, (250, 0))
road_group.add(road)

def read_record():
    with open('record.txt') as f:
        return f.readline()


def write_record(r):
    with open('record.txt', 'w') as f:
        f.write(str(r))


def spawn_road():
    road_bg = Road(road_image, (250, -600))
    road_group.add(road_bg)


def spawn_traffic():
    position = (random.randint(40, 460), random.randint(-60, -40))
    speed = random.randint(7, 20)
    traffic_car = TrafficCar(random.choice(car_images), position, speed)
    cars_group.add(traffic_car)


def draw_all():
    road_group.update()
    road_group.draw(screen)
    cars_group.update()
    cars_group.draw(screen)
    my_car.draw(screen)


def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


my_car = MyCar((300, 600), my_car_image)

sound = True
timer = False
running = True
while running:
    record = read_record()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_road_time:
            spawn_road()
        if event.type == spawn_time:
            spawn_traffic()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                sound = not sound
                if sound:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_2:
                volume -= 1
                pygame.mixer.music.set_volume(volume)
            if event.key == pygame.K_3:
                volume += 1
                pygame.mixer.music.set_volume(volume)

    screen.fill(background_color)
    if my_car.game_status == 'game':
        my_car.move()
        draw_all()
        my_car.crash(crash_sound, cars_group)
    elif my_car.game_status == 'game_over':
        end_time = pygame.time.get_ticks()
        execution_time = int(end_time - start_time) // 1000
        if timer == False:
            result = int(execution_time)
            if execution_time > int(record):
                write_record(int(execution_time))
            timer = True
        font.render_to(screen, (200, 300), 'Game Over', (255, 0, 0))
        draw_text(screen, f"времени прошло: {str(result)} секунд", 30, 'white', 500 // 2, 800 // 2 + 20)
        draw_text(screen, f"рекорд: {record} секунд", 30, 'white', 500 // 2, 800 // 2 + 60)
        if result >= int(record):
            draw_text(screen, f"УРА, НОВЫЙ РЕКОРД!", 50, 'red', 500 // 2, 800 // 2 + 120)
        else:
            draw_text(screen, f"НУ В СЛЕДУЮЩИЙ РАЗ(((", 50, 'red', 500 // 2, 800 // 2 + 120)
        pygame.display.flip()
        my_car_sound.stop()
    pygame.display.flip()
    clock1.tick(FPS1)

pygame.quit()