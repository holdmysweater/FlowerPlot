import pygame

# Инициализировать игру
pygame.init()

# Константы
MIN_WIDTH, MIN_HEIGHT = 1100, 800  # Увеличенный минимальный размер окна
GRID_SIZE = 750  # Размер сетки
PANEL_WIDTH = 200  # Уменьшенная ширина панели
PANEL_HEIGHT = 400  # Центрированная по высоте панель
PANEL_PADDING_LEFT = 50  # Отступ слева для панели, чтобы привязать ее к сетке
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
    """Рисует координатную сетку, центрированную в левой части окна."""
    global grid_start_x  # Глобальная переменная для корректного использования в draw_panel
    width, height = screen.get_size()
    grid_center_x = (width - (PANEL_WIDTH + PANEL_PADDING_LEFT)) // 2
    grid_center_y = height // 2
    grid_start_x = grid_center_x - GRID_SIZE // 2
    grid_start_y = grid_center_y - GRID_SIZE // 2
    cell_size = GRID_SIZE // 10  # Разделить сетку на 10x10 (5x5 в каждую сторону)

    # Отрисовка линий
    for i in range(11):  # 11 линий (от -5 до 5)
        x = grid_start_x + i * cell_size
        y = grid_start_y + i * cell_size
        pygame.draw.line(screen, GRID_COLOR, (x, grid_start_y), (x, grid_start_y + GRID_SIZE), 1)  # Вертикальные
        pygame.draw.line(screen, GRID_COLOR, (grid_start_x, y), (grid_start_x + GRID_SIZE, y), 1)  # Горизонтальные

    # Оси
    pygame.draw.line(screen, X_AXIS_COLOR, (grid_start_x, grid_center_y), (grid_start_x + GRID_SIZE, grid_center_y),
                     3)  # Ось X
    pygame.draw.line(screen, Y_AXIS_COLOR, (grid_center_x, grid_start_y), (grid_center_x, grid_start_y + GRID_SIZE),
                     3)  # Ось Y

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


def draw_panel():
    """Рисует боковую панель справа, привязанную к сетке с отступом слева."""
    width, height = screen.get_size()
    panel_x = grid_start_x + GRID_SIZE + PANEL_PADDING_LEFT  # Привязка к сетке
    panel_y = (height - PANEL_HEIGHT) // 2  # Центрирование панели по высоте

    # Загрузка пользовательского спрайта для фона панели
    panel_background = pygame.image.load("assets/box.jpg")  # Укажите путь к спрайту
    panel_background = pygame.transform.scale(panel_background, (PANEL_WIDTH, PANEL_HEIGHT))
    screen.blit(panel_background, (panel_x, panel_y))

    # Отображение текста с инструкцией
    instruction_text = font.render("Plant the seed at:", True, FONT_COLOR, FONT_BG_COLOR)
    screen.blit(instruction_text, (panel_x + 20, panel_y + 20))


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

    # Отрисовка панели справа
    draw_panel()

    # Обновить кадры
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
