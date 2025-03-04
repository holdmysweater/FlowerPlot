import pygame
import random

# Initialize pygame
pygame.init()

# Constants
MIN_WIDTH, MIN_HEIGHT = 1100, 800
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
GRID_CELLS = 5  # Grid goes from -5 to 5

# Load assets
BACKGROUND_IMAGE = pygame.image.load("assets/background.jpg")
PANEL_BACKGROUND = pygame.image.load("assets/box.jpg")
SEED_IMAGES = [pygame.image.load(f"assets/seed_{i}.png") for i in range(1, 6)]
FLOWER_IMAGES = [pygame.image.load(f"assets/flower_{i}.png") for i in range(1, 6)]

# Resize images
PANEL_BACKGROUND = pygame.transform.scale(PANEL_BACKGROUND, (PANEL_WIDTH, PANEL_HEIGHT))
SEED_IMAGES = [pygame.transform.scale(img, (SEED_SIZE, SEED_SIZE)) for img in SEED_IMAGES]
FLOWER_IMAGES = [pygame.transform.scale(img, (FLOWER_SIZE, FLOWER_SIZE)) for img in FLOWER_IMAGES]

# Game setup
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flower Plot")
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()


# Grid setup
def get_random_coordinate(taken_coordinates):
    possible_coords = [(x, y) for x in range(-GRID_CELLS, GRID_CELLS + 1)
                       for y in range(-GRID_CELLS, GRID_CELLS + 1)
                       if (x, y) not in taken_coordinates]
    return random.choice(possible_coords) if possible_coords else None


taken_coordinates = set()
target_coordinate = get_random_coordinate(taken_coordinates)

# Seed drag variables
selected_seed = None
seed_x, seed_y = 0, 0
seed_start_x, seed_start_y = 0, 0
hover_x, hover_y = None, None

running = True
while running:
    screen.blit(pygame.transform.scale(BACKGROUND_IMAGE, screen.get_size()), (0, 0))
    width, height = screen.get_size()
    grid_center_x = (width - (PANEL_WIDTH + PANEL_PADDING_LEFT)) // 2
    grid_center_y = height // 2
    grid_start_x = grid_center_x - GRID_SIZE // 2
    grid_start_y = grid_center_y - GRID_SIZE // 2
    cell_size = GRID_SIZE // (GRID_CELLS * 2)

    # Draw grid
    for i in range(11):
        x = grid_start_x + i * cell_size
        y = grid_start_y + i * cell_size
        pygame.draw.line(screen, GRID_COLOR, (x, grid_start_y), (x, grid_start_y + GRID_SIZE), 1)
        pygame.draw.line(screen, GRID_COLOR, (grid_start_x, y), (grid_start_x + GRID_SIZE, y), 1)

    # Draw axes
    pygame.draw.line(screen, X_AXIS_COLOR, (grid_start_x, grid_center_y), (grid_start_x + GRID_SIZE, grid_center_y), 3)
    pygame.draw.line(screen, Y_AXIS_COLOR, (grid_center_x, grid_start_y), (grid_center_x, grid_start_y + GRID_SIZE), 3)

    # Draw panel
    panel_x = grid_start_x + GRID_SIZE + PANEL_PADDING_LEFT
    panel_y = (height - PANEL_HEIGHT) // 2
    screen.blit(PANEL_BACKGROUND, (panel_x, panel_y))

    # Display instruction text
    instruction_text = font.render("Посадите семечко", True, FONT_COLOR, FONT_BG_COLOR)
    screen.blit(instruction_text, (panel_x + 20, panel_y + 30))

    # Display target coordinates
    target_text = font.render(f"Plant at: {target_coordinate}", True, FONT_COLOR, FONT_BG_COLOR)
    screen.blit(target_text, (panel_x + 5, panel_y + 350))

    # Draw occupied flowers
    for (x, y) in taken_coordinates:
        screen.blit(FLOWER_IMAGES[0], (grid_start_x + (x + 5) * cell_size - FLOWER_SIZE // 2,
                                       grid_start_y + (5 - y) * cell_size - FLOWER_SIZE // 2))

    # Draw hovered grid point
    if hover_x is not None and hover_y is not None:
        pygame.draw.circle(screen, (255, 0, 0), (hover_x, hover_y), 5)

    # Draw seed
    if selected_seed is not None:
        screen.blit(selected_seed, (seed_x, seed_y))
    else:
        screen.blit(SEED_IMAGES[0], (panel_x + (PANEL_WIDTH - SEED_SIZE) // 2, panel_y + 100))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if panel_x + (PANEL_WIDTH - SEED_SIZE) // 2 < event.pos[0] < panel_x + (
                    PANEL_WIDTH + SEED_SIZE) // 2 and panel_y + 100 < event.pos[1] < panel_y + 100 + SEED_SIZE:
                selected_seed = SEED_IMAGES[0]
                seed_x, seed_y = event.pos
                seed_start_x, seed_start_y = seed_x, seed_y
        elif event.type == pygame.MOUSEMOTION and selected_seed is not None:
            seed_x, seed_y = event.pos
            grid_x = round((seed_x - grid_start_x) / cell_size) - 5
            grid_y = 5 - round((seed_y - grid_start_y) / cell_size)
            if -5 <= grid_x <= 5 and -5 <= grid_y <= 5:
                hover_x = grid_start_x + (grid_x + 5) * cell_size
                hover_y = grid_start_y + (5 - grid_y) * cell_size
            else:
                hover_x, hover_y = None, None
        elif event.type == pygame.MOUSEBUTTONUP and selected_seed is not None:
            grid_x = round((seed_x - grid_start_x) / cell_size) - 5
            grid_y = 5 - round((seed_y - grid_start_y) / cell_size)
            if (grid_x, grid_y) == target_coordinate:
                taken_coordinates.add(target_coordinate)
                target_coordinate = get_random_coordinate(taken_coordinates)
            selected_seed = None
            hover_x, hover_y = None, None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
