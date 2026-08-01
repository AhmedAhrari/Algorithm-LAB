import pygame
import random
import sys
from collections import deque

# First Settings
WIDTH, HEIGHT = 1000, 600
BAR_WIDTH = 8
MARGIN = 10
ARRAY_SIZE = 120
MAX_VALUE = 500
FPS = 60

COLORS = {
    'BACKGROUND': (30, 30, 40),
    'BAR_DEFAULT': (100, 150, 255),
    'BAR_SWAPPING': (255, 80, 80),
    'BAR_SORTED': (80, 255, 80),
    'BAR_COMPARING': (255, 150, 50),
    'BAR_CURRENT': (200, 100, 255),
    'BAR_SHIFTING': (255, 220, 80),
    'TEXT': (255, 255, 255),
    'BUTTON': (60, 60, 80),
    'BUTTON_HOVER': (80, 80, 100),
    'BUTTON_TEXT': (220, 220, 220)
}


class InsertionSortVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Insertion Sort Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)

        self.array = []
        self.colors = []
        self.steps = deque()
        self.is_sorting = False
        self.is_paused = False
        self.speed = 30
        self.comparisons = 0
        self.shifts = 0
        self.step_count = 0

        self.buttons = []
        self.create_buttons()
        self.generate_array()

    def generate_array(self):
        self.array = [random.randint(10, MAX_VALUE) for _ in range(ARRAY_SIZE)]
        self.colors = [COLORS['BAR_DEFAULT'] for _ in range(ARRAY_SIZE)]
        self.comparisons = 0
        self.shifts = 0
        self.step_count = 0
        self.steps.clear()
        self.is_sorting = False
        self.is_paused = False

    def create_buttons(self):
        btn_width, btn_height = 100, 40
        x_start = WIDTH // 2 - 250
        y_start = HEIGHT - 80
        self.buttons = [
            {'text': 'Generate', 'x': x_start, 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Start', 'x': x_start + btn_width + 20, 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Pause', 'x': x_start + 2 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Reset', 'x': x_start + 3 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False}
        ]

    def draw_buttons(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for btn in self.buttons:
            if btn['x'] <= mouse_x <= btn['x'] + btn['w'] and btn['y'] <= mouse_y <= btn['y'] + btn['h']:
                btn['hover'] = True
                color = COLORS['BUTTON_HOVER']
            else:
                btn['hover'] = False
                color = COLORS['BUTTON']
            pygame.draw.rect(self.screen, color, (btn['x'], btn['y'], btn['w'], btn['h']))
            pygame.draw.rect(self.screen, COLORS['TEXT'], (btn['x'], btn['y'], btn['w'], btn['h']), 2)
            text = self.font.render(btn['text'], True, COLORS['BUTTON_TEXT'])
            text_rect = text.get_rect(center=(btn['x'] + btn['w'] // 2, btn['y'] + btn['h'] // 2))
            self.screen.blit(text, text_rect)

    def handle_button_click(self, pos):
        x, y = pos
        for btn in self.buttons:
            if btn['x'] <= x <= btn['x'] + btn['w'] and btn['y'] <= y <= btn['y'] + btn['h']:
                if btn['text'] == 'Generate' and not self.is_sorting:
                    self.generate_array()
                elif btn['text'] == 'Start' and not self.is_sorting:
                    self.start_sort()
                elif btn['text'] == 'Pause' and self.is_sorting:
                    self.is_paused = not self.is_paused
                elif btn['text'] == 'Reset':
                    self.is_sorting = False
                    self.is_paused = False
                    self.generate_array()
                return True
        return False

    # Generating Steps By Copy
    def start_sort(self):
        if self.is_sorting:
            return
        self.is_sorting = True
        self.is_paused = False
        self.comparisons = 0
        self.shifts = 0
        self.step_count = 0
        self.steps.clear()

        arr_copy = self.array[:]
        gen = self.insertion_sort_steps(arr_copy)
        for step in gen:
            self.steps.append(step)

        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def insertion_sort_steps(self, arr):
        n = len(arr)
        if n <= 1:
            yield ('mark_sorted', 0)
            return

        yield ('mark_sorted', 0)

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            yield ('set_current', i)

            while j >= 0 and arr[j] > key:
                self.comparisons += 1
                yield ('compare', j, j + 1)
                arr[j + 1] = arr[j]
                self.shifts += 1
                yield ('shift', j, j + 1)
                j -= 1

            if j >= 0:
                self.comparisons += 1
                yield ('compare', j, j + 1)

            arr[j + 1] = key
            if j + 1 != i:
                # Store the key value in the place_key step
                yield ('place_key', j + 1, key)

            yield ('mark_sorted', j + 1)

    # Running Steps
    def run_sort(self):
        if not self.is_sorting or self.is_paused:
            return
        if self.steps:
            step = self.steps.popleft()
            self.step_count += 1
            self.apply_step(step)
        else:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def apply_step(self, step):
        op = step[0]

        if op == 'set_current':
            _, idx = step
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'],):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx] = COLORS['BAR_CURRENT']

        elif op == 'compare':
            _, idx1, idx2 = step
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'], COLORS['BAR_CURRENT']):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx1] = COLORS['BAR_COMPARING']
            self.colors[idx2] = COLORS['BAR_COMPARING']

        elif op == 'shift':
            _, from_idx, to_idx = step
            # Actual shift ==> arr[to_idx] = arr[from_idx]
            self.array[to_idx] = self.array[from_idx]
            self.colors[from_idx] = COLORS['BAR_SHIFTING']
            self.colors[to_idx] = COLORS['BAR_SHIFTING']

        elif op == 'place_key':
            _, idx, key_value = step
            # Insert key_value into index idx
            self.array[idx] = key_value
            self.colors[idx] = COLORS['BAR_SWAPPING']  # Red to show placement

        elif op == 'mark_sorted':
            _, idx = step
            self.colors[idx] = COLORS['BAR_SORTED']

    # Draw
    def draw(self):
        self.screen.fill(COLORS['BACKGROUND'])
        for i, value in enumerate(self.array):
            x = MARGIN + i * (BAR_WIDTH + 1)
            height = (value / MAX_VALUE) * (HEIGHT - 150)
            y = HEIGHT - 100 - height
            color = self.colors[i] if i < len(self.colors) else COLORS['BAR_DEFAULT']
            pygame.draw.rect(self.screen, color, (x, y, BAR_WIDTH, height))
            pygame.draw.rect(self.screen, (40, 40, 50), (x, y, BAR_WIDTH, height), 1)

        info = f"Comparisons: {self.comparisons}  Shifts: {self.shifts}  Steps: {self.step_count}  Speed: {self.speed}"
        self.screen.blit(self.font.render(info, True, COLORS['TEXT']), (20, 20))

        status = "Sorting..." if self.is_sorting and not self.is_paused else \
                 "Paused" if self.is_paused else "Idle"
        self.screen.blit(self.big_font.render(status, True, COLORS['TEXT']), (WIDTH - 200, 20))

        self.draw_buttons()
        pygame.display.flip()

    # Main Loop
    def run(self):
        running = True
        while running:
            if self.is_sorting and not self.is_paused:
                steps_per_frame = max(1, self.speed // 30)
                for _ in range(steps_per_frame):
                    self.run_sort()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_button_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.is_sorting:
                        self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r and not self.is_sorting:
                        self.generate_array()
                    elif event.key == pygame.K_s and not self.is_sorting:
                        self.start_sort()
                    elif event.key == pygame.K_UP:
                        self.speed = min(100, self.speed + 5)
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(5, self.speed - 5)

            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    viz = InsertionSortVisualizer()
    viz.run()