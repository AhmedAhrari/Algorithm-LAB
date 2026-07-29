import pygame
import random
import sys
from collections import deque

# FIRST SETTINGS
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
    'BAR_PIVOT': (200, 100, 255),
    'BAR_SCANNING': (255, 220, 80),
    'TEXT': (255, 255, 255),
    'BUTTON': (60, 60, 80),
    'BUTTON_HOVER': (80, 80, 100),
    'BUTTON_TEXT': (220, 220, 220)
}


class QuickSortVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quick Sort Visualizer")
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
        self.swaps = 0
        self.step_count = 0

        self.buttons = []
        self.create_buttons()
        self.generate_array()

    def generate_array(self):
        self.array = [random.randint(10, MAX_VALUE) for _ in range(ARRAY_SIZE)]
        self.colors = [COLORS['BAR_DEFAULT'] for _ in range(ARRAY_SIZE)]
        self.comparisons = 0
        self.swaps = 0
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

    # Generating steps by copying
    def start_sort(self):
        if self.is_sorting:
            return
        self.is_sorting = True
        self.is_paused = False
        self.comparisons = 0
        self.swaps = 0
        self.step_count = 0
        self.steps.clear()

        # Important ===> We give a copy of the array to the generator so that the original array is not tampered with.
        arr_copy = self.array[:]
        gen = self.quick_sort_steps(0, len(self.array) - 1, arr_copy)
        for step in gen:
            self.steps.append(step)

        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def quick_sort_steps(self, low, high, arr):
        # Recursive generator that works on copy and only produces steps
        if low >= high:
            if low == high:
                yield ('mark_sorted', low)
            return

        pivot_idx = high
        yield ('set_pivot', pivot_idx)

        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            yield ('compare', j, pivot_idx)
            if arr[j] < arr[pivot_idx]:
                i += 1
                if i != j:
                    # Move on the copy (not on the original array)
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swaps += 1
                    yield ('swap', i, j)
                yield ('mark_scan', i)

        i += 1
        if i != pivot_idx:
            arr[i], arr[pivot_idx] = arr[pivot_idx], arr[i]
            self.swaps += 1
            yield ('swap', i, pivot_idx)

        yield ('mark_sorted', i)

        # Return to subarrays (with the same copy)
        yield from self.quick_sort_steps(low, i - 1, arr)
        yield from self.quick_sort_steps(i + 1, high, arr)

    # Running the steps (only here the array changes)
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
        if op == 'set_pivot':
            _, idx = step
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'],):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx] = COLORS['BAR_PIVOT']

        elif op == 'compare':
            _, idx1, idx2 = step
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'], COLORS['BAR_PIVOT']):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx1] = COLORS['BAR_COMPARING']
            self.colors[idx2] = COLORS['BAR_COMPARING']

        elif op == 'swap':
            _, idx1, idx2 = step
    
            self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]
            self.colors[idx1] = COLORS['BAR_SWAPPING']
            self.colors[idx2] = COLORS['BAR_SWAPPING']

        elif op == 'mark_scan':
            _, idx = step
            if self.colors[idx] not in (COLORS['BAR_SORTED'], COLORS['BAR_PIVOT']):
                self.colors[idx] = COLORS['BAR_SCANNING']

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

        info = f"Comparisons: {self.comparisons}  Swaps: {self.swaps}  Steps: {self.step_count}  Speed: {self.speed}"
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
    viz = QuickSortVisualizer()
    viz.run()