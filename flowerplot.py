import pygame
import random
import time

# Инициализация pygame
pygame.init()

# Константы
MIN_WIDTH, MIN_HEIGHT = 1100, 850
GRID_SIZE = 750
PANEL_WIDTH = 200
PANEL_HEIGHT = 400
PANEL_PADDING_LEFT = 50
GRID_COLOR = (255, 255, 255)
X_AXIS_COLOR = (255, 0, 0)
Y_AXIS_COLOR = (0, 255, 0)
FONT_COLOR = (255, 255, 255)
FONT_BG_COLOR = (0, 0, 0)
FONT_SIZE = 30
SEED_SIZE = 50
FLOWER_SIZE = 100
FPS = 60
GRID_CELLS = 5

# Загрузка ресурсов
BACKGROUND_IMAGE = pygame.image.load("assets/background.jpg")
PANEL_BACKGROUND = pygame.image.load("assets/box.jpg")
SEED_IMAGES = [pygame.image.load(f"assets/seed_{i}.png") for i in range(1, 6)]
FLOWER_IMAGES = [pygame.image.load(f"assets/flower_{i}.png") for i in range(1, 6)]

# Масштабирование изображений
PANEL_BACKGROUND = pygame.transform.scale(PANEL_BACKGROUND, (PANEL_WIDTH, PANEL_HEIGHT))
SEED_IMAGES = [pygame.transform.scale(img, (SEED_SIZE, SEED_SIZE)) for img in SEED_IMAGES]
FLOWER_IMAGES = [pygame.transform.scale(img, (FLOWER_SIZE, FLOWER_SIZE)) for img in FLOWER_IMAGES]

# Настройка игры
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flower Plot")
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()


def get_random_coordinate(taken_coordinates):
    """Получить случайную координату для посадки."""
    possible_coords = [(x, y) for x in range(-GRID_CELLS, GRID_CELLS + 1)
                       for y in range(-GRID_CELLS, GRID_CELLS + 1)
                       if (x, y) not in taken_coordinates]
    return random.choice(possible_coords) if possible_coords else None


def get_elapsed_time():
    """Получить время, прошедшее с начала игры."""
    if timer_started and not game_won:
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{minutes}:{seconds:02d}"
    return "0:00"


def reset_game():
    """Сброс состояния игры."""
    global taken_coordinates, target_coordinate, selected_seed, selected_seed_index
    global seed_x, seed_y, current_seed_index, timer_started, start_time
    global planted_count, error_count, game_won

    taken_coordinates = {}
    target_coordinate = get_random_coordinate(taken_coordinates)
    selected_seed = None
    selected_seed_index = None
    seed_x, seed_y = 0, 0
    current_seed_index = random.randint(0, 4)
    timer_started = False
    start_time = 0
    planted_count = 0
    error_count = 0
    game_won = False


def draw_grid(grid_start_x, grid_start_y, cell_size, grid_center_x, grid_center_y):
    """Отрисовка сетки с цветами и осей координат."""
    for (x, y), flower_index in taken_coordinates.items():
        screen.blit(FLOWER_IMAGES[flower_index], (grid_start_x + (x + 5) * cell_size - FLOWER_SIZE // 2,
                                                  grid_start_y + (5 - y) * cell_size - FLOWER_SIZE // 2))

    for i in range(11):
        x = grid_start_x + i * cell_size
        y = grid_start_y + i * cell_size
        pygame.draw.line(screen, GRID_COLOR, (x, grid_start_y), (x, grid_start_y + GRID_SIZE), 1)
        pygame.draw.line(screen, GRID_COLOR, (grid_start_x, y), (grid_start_x + GRID_SIZE, y), 1)

    pygame.draw.line(screen, X_AXIS_COLOR, (grid_start_x, grid_center_y), (grid_start_x + GRID_SIZE, grid_center_y), 3)
    pygame.draw.line(screen, Y_AXIS_COLOR, (grid_center_x, grid_start_y), (grid_center_x, grid_start_y + GRID_SIZE), 3)

    # Добавление стрелок на осях
    pygame.draw.polygon(screen, X_AXIS_COLOR, [
        (grid_start_x + GRID_SIZE + 5, grid_center_y),
        (grid_start_x + GRID_SIZE - 10, grid_center_y - 5),
        (grid_start_x + GRID_SIZE - 10, grid_center_y + 5)
    ])  # X-стрелка

    pygame.draw.polygon(screen, Y_AXIS_COLOR, [
        (grid_center_x, grid_start_y - 5),
        (grid_center_x - 5, grid_start_y + 10),
        (grid_center_x + 5, grid_start_y + 10)
    ])  # Y-стрелка

    # Добавление чисел на осях
    for i in range(-5, 6):
        x_text = font.render(str(i), True, FONT_COLOR, FONT_BG_COLOR)
        y_text = font.render(str(i), True, FONT_COLOR, FONT_BG_COLOR)

        if i != 0:
            x_pos = grid_start_x + (i + 5) * cell_size - (x_text.get_width() // 2)
            y_pos = grid_center_y + 5
            screen.blit(x_text, (x_pos, y_pos))  # Числа на оси X

            x_pos = grid_center_x + 5
            y_pos = grid_start_y + (5 - i) * cell_size - (y_text.get_height() // 2)
            screen.blit(y_text, (x_pos, y_pos))  # Числа на оси Y
        else:
            zero_text = font.render("0", True, FONT_COLOR, FONT_BG_COLOR)
            screen.blit(zero_text, (grid_center_x + 5, grid_center_y + 5))  # 0 в центре


def draw_panel(panel_x, panel_y):
    """Отрисовка панели с информацией."""
    screen.blit(PANEL_BACKGROUND, (panel_x, panel_y))
    instruction_text = font.render("Посадите семечко", True, FONT_BG_COLOR, FONT_COLOR)
    screen.blit(instruction_text, (panel_x + 10, panel_y + 30))
    target_text = font.render(f"в точке: {target_coordinate}", True, FONT_BG_COLOR, FONT_COLOR)
    screen.blit(target_text, (panel_x + 30, panel_y + 350))

    time_text = font.render(f"Время: {get_elapsed_time()}", True, FONT_COLOR, FONT_BG_COLOR)
    planted_text = font.render(f"Посажено: {planted_count}", True, FONT_COLOR, FONT_BG_COLOR)
    errors_text = font.render(f"Количество ошибок: {error_count}", True, FONT_COLOR, FONT_BG_COLOR)

    screen.blit(time_text, (width - 250, 20))
    screen.blit(planted_text, (width - 250, 60))
    screen.blit(errors_text, (width - 250, 100))

def handle_events():
    """Обработка событий игры."""
    global running, selected_seed, seed_x, seed_y, selected_seed_index
    global current_seed_index, timer_started, start_time, target_coordinate
    global planted_count, error_count, game_won

    if game_won:
        win_text = font.render("Ты выиграл!", True, FONT_COLOR, FONT_BG_COLOR)
        restart_text = font.render("Нажмите R, чтобы сыграть заново", True, FONT_COLOR, FONT_BG_COLOR)
        screen.blit(win_text, ((width - win_text.get_width()) // 2, height // 2 - 40))
        screen.blit(restart_text, ((width - restart_text.get_width()) // 2, height // 2 + 10))
    else:
        if selected_seed is not None:
            screen.blit(selected_seed, (seed_x, seed_y))
        else:
            screen.blit(SEED_IMAGES[current_seed_index], (panel_x + (PANEL_WIDTH - SEED_SIZE) // 2, panel_y + 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_won:
            reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
            if panel_x < event.pos[0] < panel_x + PANEL_WIDTH and panel_y < event.pos[1] < panel_y + PANEL_HEIGHT:
                selected_seed_index = current_seed_index
                selected_seed = SEED_IMAGES[selected_seed_index]
                seed_x, seed_y = event.pos
                if not timer_started:
                    timer_started = True
                    start_time = time.time()
        elif event.type == pygame.MOUSEMOTION and selected_seed is not None:
            seed_x, seed_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and selected_seed is not None:
            grid_x = round((seed_x - grid_start_x) / cell_size) - 5
            grid_y = 5 - round((seed_y - grid_start_y) / cell_size)
            if (grid_x, grid_y) == target_coordinate:
                taken_coordinates[target_coordinate] = selected_seed_index
                planted_count += 1
                target_coordinate = get_random_coordinate(taken_coordinates)
                current_seed_index = random.randint(0, 4)
                if target_coordinate is None:
                    game_won = True
            else:
                error_count += 1
            selected_seed = None


reset_game()
running = True
while running:
    screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, screen.get_size()), (0, 0))
    width, height = screen.get_size()
    grid_center_x = (width - (PANEL_WIDTH + PANEL_PADDING_LEFT)) // 2
    grid_center_y = height // 2
    grid_start_x = grid_center_x - GRID_SIZE // 2
    grid_start_y = grid_center_y - GRID_SIZE // 2
    cell_size = GRID_SIZE // (GRID_CELLS * 2)
    panel_x = grid_start_x + GRID_SIZE + PANEL_PADDING_LEFT
    panel_y = (height - PANEL_HEIGHT) // 2

    draw_grid(grid_start_x, grid_start_y, cell_size, grid_center_x, grid_center_y)
    draw_panel(panel_x, panel_y)
    handle_events()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
