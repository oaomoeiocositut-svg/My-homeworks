import pygame
import sys

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер: анимация персонажа")

#  фон
try:
    bg_image = pygame.image.load("back_font.jpg").convert()
except FileNotFoundError:
    print("Ошибка: Файл 'back_font.jpg' не найден!")
    pygame.quit()
    sys.exit()

# Подгоняем фон по высоте окна
scale_factor = HEIGHT / bg_image.get_height()
new_width = int(bg_image.get_width() * scale_factor)
bg_image = pygame.transform.scale(bg_image, (new_width, HEIGHT))
bg_width = bg_image.get_width()

#  персонаж
try:
    sprite_sheet = pygame.image.load("char_blue.png").convert_alpha()
except FileNotFoundError:
    print("Ошибка: Файл 'char_blue.png' не найден!")
    print("Положите char_blue.png рядом с pygame_homework_animated.py")
    pygame.quit()
    sys.exit()

# длина-ширина персонажа
FRAME_WIDTH = 56
FRAME_HEIGHT = 56

# Ряд 0 — спокойная анимация (6 кадров)
idle_frames = []
for i in range(6):
    frame = sprite_sheet.subsurface(
        pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    ).copy()
    idle_frames.append(frame)

# Ряд 2 — анимация движения (8 кадров)
walk_frames_right = []
for i in range(8):
    frame = sprite_sheet.subsurface(
        pygame.Rect(i * FRAME_WIDTH, 2 * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
    ).copy()
    walk_frames_right.append(frame)

# Отражённые кадры для движения влево
walk_frames_left = [
    pygame.transform.flip(frame, True, False)
    for frame in walk_frames_right
]

# настройка игрока и его физика
player_width = 56
player_height = 56
player_speed = 5

# начальная точка спавна персонажа
world_x = 0
player_y = 50

# геометрия (а не, это физика)
player_vel_y = 0
gravity = 0.5

# Уровень земли (пока что первый)
GROUND_LEVEL = HEIGHT - 50

# --- АНИМАЦИЯ ---
current_frame = 0
animation_timer = 0
animation_speed = 90  # Чем меньше число — тем быстрее анимация

# Направление персонажа
facing_right = True

clock = pygame.time.Clock()

while True:
    # --- СОБЫТИЯ ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- УПРАВЛЕНИЕ ---
    keys = pygame.key.get_pressed()

    moving = False

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        world_x -= player_speed
        moving = True
        facing_right = False

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        world_x += player_speed
        moving = True
        facing_right = True

    # геометрия игрока (а не, это физика игрока)
    player_vel_y += gravity
    player_y += player_vel_y

    # Проверка столкновения с землёй
    if player_y + player_height >= GROUND_LEVEL:
        player_y = GROUND_LEVEL - player_height
        player_vel_y = 0

    # --- АНИМАЦИЯ ---
    # clock.get_time() показывает, сколько миллисекунд прошло
    # с прошлого кадра игры.
    animation_timer += clock.get_time()

    if moving:
        if animation_timer >= animation_speed:
            current_frame += 1

            if current_frame >= len(walk_frames_right):
                current_frame = 0

            animation_timer = 0
    else:
        # Когда игрок стоит, показываем спокойную анимацию
        if animation_timer >= animation_speed:
            current_frame += 1

            if current_frame >= len(idle_frames):
                current_frame = 0

            animation_timer = 0

    # --- ОТРИСОВКА ФОНА ---
    offset_x = -world_x % bg_width

    for x in range(int(offset_x) - bg_width, WIDTH, bg_width):
        screen.blit(bg_image, (x, 0))

    # --- ВЫБИРАЕМ КАДР ПЕРСОНАЖА ---
    if moving:
        if facing_right:
            player_image = walk_frames_right[current_frame]
        else:
            player_image = walk_frames_left[current_frame]
    else:
        player_image = idle_frames[current_frame % len(idle_frames)]
    # Игрок всегда находится примерно в центре экрана
    player_screen_x = (WIDTH // 2) - (player_width // 2)

    screen.blit(player_image, (player_screen_x, player_y))

    # Обновление экрана
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)


pygame.quit()
