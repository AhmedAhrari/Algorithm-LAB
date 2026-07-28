import pygame
import random
import sys

# Window
WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 10
MARGIN = 2
NUM_BARS = WIDTH // (BAR_WIDTH + MARGIN)    # Number of bars

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

def generate_data():   
    """Generate a list of random numbers for the heights of the bars"""
    return [random.randint(10, HEIGHT - 50) for _ in range(NUM_BARS)]

def draw_bars(screen, data, color_positions=None):
    screen.fill(BLACK)
    if color_positions is None:
        color_positions = []
    for i, height in enumerate(data):
        x = i * (BAR_WIDTH + MARGIN) + MARGIN
        y = HEIGHT - height
        color = RED if i in color_positions else BLUE
        pygame.draw.rect(screen, color, (x, y, BAR_WIDTH, height))
    pygame.display.flip()

def bubble_sort_visual(screen, data):
    # Run Algorithm With Animation
    n = len(data)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # RED ==> Comparables
            draw_bars(screen, data, color_positions=[j, j+1])

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                pygame.time.delay(30)
            else:
                pygame.time.delay(20)

        if not swapped:
            break

    # GREEN ==> Final Result
    for i in range(len(data)):
        draw_bars(screen, data, color_positions=[i])
        pygame.time.delay(10)
    draw_bars(screen, data)

def main():
    # START PYGAME
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bubble Sort Visualization - Pygame")
    clock = pygame.time.Clock()

    data = generate_data()   # ← نام تابع باید دقیقاً با تعریف مطابقت داشته باشد
    running = True
    sorting_started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not sorting_started:
                    sorting_started = True
                    bubble_sort_visual(screen, data)
                    sorting_started = False
                if event.key == pygame.K_r:
                    data = generate_data()
                    draw_bars(screen, data)

        if not sorting_started:
            draw_bars(screen, data)

        clock.tick(60)      # 60 Frame Per-Second

    pygame.quit()

if __name__ == "__main__":
    main()