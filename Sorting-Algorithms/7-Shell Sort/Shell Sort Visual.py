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

# COLOR PALLETS
COLORS = {
    'BACKGROUND': (30, 30, 40),
    'BAR_DEFAULT': (100, 150, 255),
    'BAR_SWAPPING': (255, 80, 80),       # Move/Shift
    'BAR_SORTED': (80, 255, 80),
    'BAR_COMPARING': (255, 150, 50),
    'BAR_CURRENT': (200, 100, 255),      # Key element (key)
    'BAR_SHIFTING': (255, 220, 80),      # Shifted Elements
    'BAR_GAP': (0, 200, 200),            # Elements that are in the current gap (optional)
    'TEXT': (255, 255, 255),
    'BUTTON': (60, 60, 80),
    'BUTTON_HOVER': (80, 80, 100),
    'BUTTON_TEXT': (220, 220, 220)
}


class ShellSortVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shell Sort Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)

        # Main Data
        self.array = []
        self.colors = []
        self.steps = deque()
        self.is_sorting = False
        self.is_paused = False
        self.speed = 30
        self.comparisons = 0
        self.shifts = 0
        self.step_count = 0
        self.current_gap = 0  # To display in the title

        # Buttons
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
        self.current_gap = 0

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
        self.current_gap = 0

        # Copy for Generate Steps
        arr_copy = self.array[:]
        gen = self.shell_sort_steps(arr_copy)
        for step in gen:
            self.steps.append(step)

        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def shell_sort_steps(self, arr):
    
        n = len(arr)
        # Sequence of chats (divided by 2)
        gap = n // 2
        while gap > 0:
            self.current_gap = gap
            yield ('set_gap', gap)

            # Sort within each subarray with gap
            for i in range(gap, n):
                key = arr[i]
                j = i - gap

                yield ('set_current', i)   # Show key element (with space)

                while j >= 0 and arr[j] > key:
                    self.comparisons += 1
                    yield ('compare', j, j + gap)   # Compare arr[j] with arr[j+gap]

                    # Shift arr[j] right (with space)
                    arr[j + gap] = arr[j]
                    self.shifts += 1
                    yield ('shift', j, j + gap)
                    j -= gap

                if j >= 0:
                    self.comparisons += 1
                    yield ('compare', j, j + gap)

                # Putting the key in the right place
                arr[j + gap] = key
                if j + gap != i:
                    yield ('place_key', j + gap, key)

                # After each insertion, the j+gap element (and the rest of the subarray) may not be sorted, but we don't turn it green for display
                # In Shell Sort, it only sorts at the end of the entire array, so we don't mark it as sorted for now

            gap //= 2

        # After all the chats are finished ===> The array is completely sorted.
        for i in range(n):
            yield ('mark_sorted', i)

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

        if op == 'set_gap':
            _, gap = step
            self.current_gap = gap
            # We can highlight elements related to this gap (optional)
            # For simplicity, we just keep gap in a variable and show it in the view
        elif op == 'set_current':
            _, idx = step
            # بازنشانی رنگ‌های غیرمرتبط (به جز عناصر سبز)
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'],):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx] = COLORS['BAR_CURRENT']

        elif op == 'compare':
            _, idx1, idx2 = step
            # idx1: previous element in subarray
            # idx2: current element (with space)
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
            self.array[idx] = key_value
            self.colors[idx] = COLORS['BAR_SWAPPING']  # Red to show placement

        elif op == 'mark_sorted':
            _, idx = step
            self.colors[idx] = COLORS['BAR_SORTED']

    # Draw
    def draw(self):
        self.screen.fill(COLORS['BACKGROUND'])

        # Draw Bars
        for i, value in enumerate(self.array):
            x = MARGIN + i * (BAR_WIDTH + 1)
            height = (value / MAX_VALUE) * (HEIGHT - 150)
            y = HEIGHT - 100 - height
            color = self.colors[i] if i < len(self.colors) else COLORS['BAR_DEFAULT']
            pygame.draw.rect(self.screen, color, (x, y, BAR_WIDTH, height))
            pygame.draw.rect(self.screen, (40, 40, 50), (x, y, BAR_WIDTH, height), 1)

        # Show Information
        info = f"Comparisons: {self.comparisons}  Shifts: {self.shifts}  Steps: {self.step_count}  Speed: {self.speed}"
        self.screen.blit(self.font.render(info, True, COLORS['TEXT']), (20, 20))

        # Display the current gap
        gap_text = f"Gap: {self.current_gap}"
        self.screen.blit(self.font.render(gap_text, True, COLORS['TEXT']), (WIDTH - 300, 20))

        status = "Sorting..." if self.is_sorting and not self.is_paused else \
                 "Paused" if self.is_paused else "Idle"
        self.screen.blit(self.big_font.render(status, True, COLORS['TEXT']), (WIDTH - 200, 50))

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
    viz = ShellSortVisualizer()
    viz.run()