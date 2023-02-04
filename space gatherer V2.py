import pygame
import random

WIDTH, HEIGHT = 600, 880
BG_COLOR = 0, 0, 0
FONT_COLOR = 255, 255, 255
STAR_COUNT = 1001  # csillagok száma
COLUMN_COUNT = 3  # minél több, annál nehezebb
SPEED = 3  # pontok sebessége (max 10)
SHIP_HEIGHT = HEIGHT - HEIGHT / 10
FUNKY = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# csillagok adatainak rögzítése
stars = []
star_color = []
for _ in range(STAR_COUNT):
    stars.append((random.randint(0, WIDTH), random.randint(0, HEIGHT), 1, 1))
    if not FUNKY:
        brightness = random.randint(30, 255)
        star_color.append((brightness, brightness, brightness))

# oszlopok létrehozása
columns = []
for index in range(1, COLUMN_COUNT + 1):
    columns.append(int(WIDTH / (COLUMN_COUNT + 1) * index))

# textúrák betöltése
ship_surf = pygame.image.load('img/ship_sidesC.png').convert_alpha()
point_surf = pygame.image.load('img/ship_B.png').convert_alpha()
points_rect = []

# feliratok
game_font = pygame.font.SysFont('consolas', 20)
title_surf = game_font.render('SPACE GATHERER', True, FONT_COLOR)
title_rect = title_surf.get_rect(center=(WIDTH / 2, HEIGHT / 10 * 3))
run_surf = game_font.render('Nyomd meg a FEL nyilat a kezdéshez', True, FONT_COLOR)
run_rect = run_surf.get_rect(center=(WIDTH / 2, HEIGHT / 10 * 4))

initial_point_rate = 60  # új pontok gyakorisága
difficulty_rate = 180  # játék nehezedésének sebessége
ship_col = 0  # kezdőoszlop
score = 0
point_timer, difficulty_timer = 0, 0
point_rate = initial_point_rate
game_active = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # irányítás
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT] and ship_col < COLUMN_COUNT - 1:
                ship_col += 1
            if pygame.key.get_pressed()[pygame.K_LEFT] and ship_col > 0:
                ship_col -= 1
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                ship_col = COLUMN_COUNT - (ship_col + 1)

    # háttér megjelenítése
    screen.fill(BG_COLOR)
    if not FUNKY:
        for index, star in enumerate(stars):
            pygame.draw.rect(screen, star_color[index], star)
    else:
        for star in stars:
            pygame.draw.rect(screen, (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255)), star)

    # aktív játék
    if game_active:

        # játék nehezítése
        if difficulty_timer > difficulty_rate:
            point_rate -= 1
            difficulty_timer = 0

        # pontok
        if point_timer > point_rate:
            points_rect.append(point_surf.get_rect(midbottom=(columns[random.randint(0, COLUMN_COUNT - 1)], 0)))
            point_timer = 0
        for index, point_rect in enumerate(points_rect):
            point_rect.centery += SPEED
            if SHIP_HEIGHT - 4 < point_rect.centery < SHIP_HEIGHT + 7 and point_rect.centerx == columns[ship_col]:
                del points_rect[index]
                score += 1
            if point_rect.centery + 17 > HEIGHT:
                game_active = False
            screen.blit(point_surf, point_rect)

        # hajó megjelenítése
        ship_rect = ship_surf.get_rect(center=(columns[ship_col], SHIP_HEIGHT))
        screen.blit(ship_surf, ship_rect)

        # felirat megjelenítése
        if score:
            score_surf = game_font.render('SCORE: ' + str(score), True, FONT_COLOR)
            score_rect = score_surf.get_rect(bottomleft=(5, HEIGHT - 5))
            screen.blit(score_surf, score_rect)

        # képkockák számlálása
        point_timer += 1
        difficulty_timer += 1

    # kezdő- és záróképernyő
    else:
        screen.blit(title_surf, title_rect)
        screen.blit(ship_surf, ship_surf.get_rect(center=(columns[ship_col], SHIP_HEIGHT)))
        screen.blit(run_surf, run_rect)

        # elért pontszám megjelenítése
        if score:
            score_surf = game_font.render('SCORE: ' + str(score), True, FONT_COLOR)
            score_rect = score_surf.get_rect(bottomleft=(5, HEIGHT - 5))
            screen.blit(score_surf, score_rect)

        # játék indítása
        if pygame.key.get_pressed()[pygame.K_UP]:
            score = 0
            point_timer, difficulty_timer = 0, 0
            points_rect = []
            point_rate = initial_point_rate
            game_active = True

    pygame.display.update()
    clock.tick(60)
pygame.quit()
