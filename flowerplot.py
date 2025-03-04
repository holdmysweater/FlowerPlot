import pygame

# Инициализировать игру
pygame.init()

# Константы
MIN_WIDTH, MIN_HEIGHT = 800, 800  # Минимальный размер окна
GRID_SIZE = 750  # Размер сетки
GRID_COLOR = (255, 255, 255)  # Белый цвет для сетки
X_AXIS_COLOR = (255, 0, 0)  # Красный для X
Y_AXIS_COLOR = (0, 255, 0)  # Зеленый для Y
FONT_COLOR = (255, 255, 255)  # Белый для чисел
FONT_BG_COLOR = (0, 0, 0)  # Черный фон под числами
FONT_SIZE = 30  # Увеличенный размер шрифта
FPS = 60


def resize_background():
    width, height = screen.get_size()
    return pygame.transform.scale(BACKGROUND_IMAGE, (width, height))


def draw_grid():
    """Рисует координатную сетку, центрированную в окне."""
    width, height = screen.get_size()
    center_x, center_y = width // 2, height // 2
    grid_start_x = center_x - GRID_SIZE // 2
    grid_start_y = center_y - GRID_SIZE // 2
    cell_size = GRID_SIZE // 10  # Разделить сетку на 10x10 (5x5 в каждую сторону)

    # Отрисовка линий
    for i in range(11):  # 11 линий (от -5 до 5)
        x = grid_start_x + i * cell_size
        y = grid_start_y + i * cell_size
        pygame.draw.line(screen, GRID_COLOR, (x, grid_start_y), (x, grid_start_y + GRID_SIZE), 1)  # Вертикальные
        pygame.draw.line(screen, GRID_COLOR, (grid_start_x, y), (grid_start_x + GRID_SIZE, y), 1)  # Горизонтальные

    # Оси
    pygame.draw.line(screen, X_AXIS_COLOR, (grid_start_x, center_y), (grid_start_x + GRID_SIZE, center_y), 3)  # Ось X
    pygame.draw.line(screen, Y_AXIS_COLOR, (center_x, grid_start_y), (center_x, grid_start_y + GRID_SIZE), 3)  # Ось Y

    # Добавление стрелок на осях
    pygame.draw.polygon(screen, X_AXIS_COLOR, [
        (grid_start_x + GRID_SIZE + 5, center_y),
        (grid_start_x + GRID_SIZE - 10, center_y - 5),
        (grid_start_x + GRID_SIZE - 10, center_y + 5)
    ])  # X-стрелка

    pygame.draw.polygon(screen, Y_AXIS_COLOR, [
        (center_x, grid_start_y - 5),
        (center_x - 5, grid_start_y + 10),
        (center_x + 5, grid_start_y + 10)
    ])  # Y-стрелка

    # Добавление чисел на осях
    for i in range(-5, 6):
        x_text = font.render(str(i), True, FONT_COLOR, FONT_BG_COLOR)
        y_text = font.render(str(i), True, FONT_COLOR, FONT_BG_COLOR)

        if i != 0:
            x_pos = grid_start_x + (i + 5) * cell_size - (x_text.get_width() // 2)
            y_pos = center_y + 5
            screen.blit(x_text, (x_pos, y_pos))  # Числа на оси X

            x_pos = center_x + 5
            y_pos = grid_start_y + (5 - i) * cell_size - (y_text.get_height() // 2)
            screen.blit(y_text, (x_pos, y_pos))  # Числа на оси Y
        else:
            zero_text = font.render("0", True, FONT_COLOR, FONT_BG_COLOR)
            screen.blit(zero_text, (center_x + 5, center_y + 5))  # 0 в центре


# Создать окно (изменяемый размер, но не меньше MIN_WIDTH x MIN_HEIGHT)
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flower Plot")

# Загрузка заднего фона
BACKGROUND_IMAGE = pygame.image.load("assets/background.jpg")

# Установить начальный фон
background = resize_background()

# Шрифт для чисел
font = pygame.font.Font(None, FONT_SIZE)

# Игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Проверка текущего размера окна
    width, height = screen.get_size()
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        width, height = max(width, MIN_WIDTH), max(height, MIN_HEIGHT)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Обновить фон, чтобы он всегда соответствовал размеру окна
    background = resize_background()

    # Прорисовка заднего фона
    screen.blit(background, (0, 0))

    # Отрисовка сетки
    draw_grid()

    # Обновить кадры
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
