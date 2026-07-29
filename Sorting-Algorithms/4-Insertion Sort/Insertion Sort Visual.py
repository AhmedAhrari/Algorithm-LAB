import pygame
import random
import sys
from collections import deque

# FIRST CONFIG SETTINGS
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
    'BAR_SWAPPING': (255, 80, 80),
    'BAR_SORTED': (80, 255, 80),
    'BAR_COMPARING': (255, 150, 50),
    'BAR_CURRENT': (200, 100, 255),      # The current element that is to be placed in the correct position
    'BAR_SHIFTING': (255, 220, 80),      # Elements that shift to the right
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

        # MAIN DATA
        self.array = []
        self.colors = []
        self.steps = deque()
        self.is_sorting = False
        self.is_paused = False
        self.speed = 30
        self.comparisons = 0
        self.shifts = 0       # Count of Shifts
        self.step_count = 0

        # دکمه‌هاBUTTONS
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
            {'text': 'Start', 'x': x_start + btn_width + 20, 'y': y_start, 'w': btn_width, 'h': btn_height,'hover': False},
            {'text': 'Pause', 'x': x_start + 2 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height,'hover': False},
            {'text': 'Reset', 'x': x_start + 3 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height,'hover': False}
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
                if btn['text'] == 'Generate':
                    if not self.is_sorting:
                        self.generate_array()
                elif btn['text'] == 'Start':
                    if not self.is_sorting:
                        self.start_sort()
                elif btn['text'] == 'Pause':
                    if self.is_sorting:
                        self.is_paused = not self.is_paused
                elif btn['text'] == 'Reset':
                    self.is_sorting = False
                    self.is_paused = False
                    self.generate_array()
                return True
        return False

    # Generative Steps of Insertion Sort
    def start_sort(self):
        if self.is_sorting:
            return

        self.is_sorting = True
        self.is_paused = False
        self.comparisons = 0
        self.shifts = 0
        self.step_count = 0
        self.steps.clear()

        generator = self.generate_steps()
        for step in generator:
            self.steps.append(step)

        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def generate_steps(self):
        """ژنراتور گام‌های Insertion Sort"""
        n = len(self.array)
        arr = self.array[:]  # Copy for simulation

        yield ('mark_sorted', 0)

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            # Show the current element (key) in purple
            yield ('set_current', i)

            # Shifting Loop
            while j >= 0 and arr[j] > key:
                self.comparisons += 1
                
                yield ('compare', j, j + 1)

                
                arr[j + 1] = arr[j]
                self.shifts += 1
                yield ('shift', j, j + 1)  
                j -= 1

            # If exited from the loop, an additional comparison (if any) to display
            if j >= 0:
                self.comparisons += 1
                yield ('compare', j, j + 1)

        
            arr[j + 1] = key
            if j + 1 != i:
                
                yield ('place_key', j + 1, i)

            # Element i (and all previous elements) are now sorted
            # but we only turn element j+1 green (because they were already green)
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
            # Reset unrelated colors (except green elements)
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'],):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx] = COLORS['BAR_CURRENT']

        elif op == 'compare':
            _, idx1, idx2 = step
            # idx1: previous element, idx2: current element (being compared)
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'], COLORS['BAR_CURRENT']):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            # Keep idx1 orange (comparable) and idx2 orange (or CURRENT)
            self.colors[idx1] = COLORS['BAR_COMPARING']
            self.colors[idx2] = COLORS['BAR_COMPARING']

        elif op == 'shift':
            _, from_idx, to_idx = step
            # Shifting: element is moved from from_idx to to_idx
            # i.e. arr[from_idx] is copied to arr[to_idx] (actually a move)
            # In the actual array, we do a shift: arr[to_idx] = arr[from_idx]
            self.array[to_idx] = self.array[from_idx]
            # Change the color of the shifted element to yellow
            self.colors[from_idx] = COLORS['BAR_SHIFTING']
            self.colors[to_idx] = COLORS['BAR_SHIFTING']

        elif op == 'place_key':
            _, idx, original_idx = step
            
            # Put key (which was originally in original_idx) in idx
            # We already kept key in variable, but it's just for show here
            # The value of key is arr[original_idx], but we put it in arr[idx]
            # Since we don't have key in the actual array, we use the original value
            # For simplicity, we don't do anything because the array is already prepared by shifts
        
            pass

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

        info_text = (f"Comparisons: {self.comparisons}  Shifts: {self.shifts}  "
                     f"Steps: {self.step_count}  Speed: {self.speed} steps/sec")
        text_surface = self.font.render(info_text, True, COLORS['TEXT'])
        self.screen.blit(text_surface, (20, 20))

        status = "Sorting..." if self.is_sorting and not self.is_paused else \
                 "Paused" if self.is_paused else "Idle"
        status_surface = self.big_font.render(status, True, COLORS['TEXT'])
        self.screen.blit(status_surface, (WIDTH - 200, 20))

        self.draw_buttons()

        pygame.display.flip()

    # Main Loop
    def run(self):
        running = True
        while running:
            if self.is_sorting and not self.is_paused:
                steps_to_run = max(1, self.speed // 30)
                for _ in range(steps_to_run):
                    self.run_sort()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_button_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.is_sorting:
                            self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r:
                        if not self.is_sorting:
                            self.generate_array()
                    elif event.key == pygame.K_s:
                        if not self.is_sorting:
                            self.start_sort()
                    elif event.key == pygame.K_UP:
                        self.speed = min(100, self.speed + 5)
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(5, self.speed - 5)

            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = InsertionSortVisualizer()
    visualizer.run()