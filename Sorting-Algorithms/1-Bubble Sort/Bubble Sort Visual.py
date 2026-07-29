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

# COLOR PALLET
COLORS = {
    'BACKGROUND': (30, 30, 40),
    'BAR_DEFAULT': (100, 150, 255),
    'BAR_SWAPPING': (255, 80, 80),
    'BAR_SORTED': (80, 255, 80),
    'BAR_COMPARING': (255, 150, 50),
    'TEXT': (255, 255, 255),
    'BUTTON': (60, 60, 80),
    'BUTTON_HOVER': (80, 80, 100),
    'BUTTON_TEXT': (220, 220, 220)
}


class BubbleSortVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bubble Sort Visualizer")
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
        self.swaps = 0
        self.step_count = 0

        # Buttons
        self.buttons = []
        self.create_buttons()

        # Generate initial random array
        self.generate_array()

    def generate_array(self):
        # Generate Array With Random Numbers
        self.array = [random.randint(10, MAX_VALUE) for _ in range(ARRAY_SIZE)]
        self.colors = [COLORS['BAR_DEFAULT'] for _ in range(ARRAY_SIZE)]
        self.comparisons = 0
        self.swaps = 0
        self.step_count = 0
        self.steps.clear()
        self.is_sorting = False
        self.is_paused = False

    def create_buttons(self):
        # Create Control Button
        btn_width, btn_height = 100, 40
        x_start = WIDTH // 2 - 250
        y_start = HEIGHT - 80

        self.buttons = [
            {'text': 'Generate', 'x': x_start, 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Start', 'x': x_start + btn_width + 20, 'y': y_start, 'w': btn_width, 'h': btn_height,
             'hover': False},
            {'text': 'Pause', 'x': x_start + 2 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height,
             'hover': False},
            {'text': 'Reset', 'x': x_start + 3 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height,
             'hover': False}
        ]

    def draw_buttons(self):
        # Draw Button
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
        # Management Click On Button
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

    # Generate Bubble Sort Steps
    def start_sort(self):
        # Starting the sorting process ===> generating steps and storing in the queue
        if self.is_sorting:
            return

        self.is_sorting = True
        self.is_paused = False
        self.comparisons = 0
        self.swaps = 0
        self.step_count = 0
        self.steps.clear()

        # Generate Steps Using Generator
        generator = self.generate_steps()
        for step in generator:
            self.steps.append(step)

        # If Not Generate Step
        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def generate_steps(self):
        """ژنراتور گام‌های Bubble Sort"""
        n = len(self.array)
        arr = self.array[:]  

        for i in range(n - 1):
            # Each pass, a large element goes to the end
            for j in range(n - 1 - i):
                # Comparison stage
                self.comparisons += 1
                yield ('compare', j, j + 1)

                if arr[j] > arr[j + 1]:
                    # Displacement
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    yield ('swap', j, j + 1)

                # Each comparison counts as a step (for counting)
                yield ('step_done',)

            
            sorted_index = n - 1 - i
            yield ('mark_sorted', sorted_index)

        # Finally, all elements are sorted (to be sure)
        for idx in range(n):
            yield ('mark_sorted', idx)

    # Implementation of steps
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

        if op == 'compare':
            _, idx1, idx2 = step
            # Reset unrelated colors (except sorted elements)
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'],):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx1] = COLORS['BAR_COMPARING']
            self.colors[idx2] = COLORS['BAR_COMPARING']

        elif op == 'swap':
            _, idx1, idx2 = step
            # Actual movement in the array
            self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]
            # Change color to red to indicate displacement
            self.colors[idx1] = COLORS['BAR_SWAPPING']
            self.colors[idx2] = COLORS['BAR_SWAPPING']

        elif op == 'step_done':
            # Just for counting steps (does nothing)
            pass

        elif op == 'mark_sorted':
            _, idx = step
            self.colors[idx] = COLORS['BAR_SORTED']

    # DRAW
    def draw(self):
        """رسم همه‌ی عناصر صفحه"""
        self.screen.fill(COLORS['BACKGROUND'])

        # Draw Bars
        for i, value in enumerate(self.array):
            x = MARGIN + i * (BAR_WIDTH + 1)
            height = (value / MAX_VALUE) * (HEIGHT - 150)
            y = HEIGHT - 100 - height
            color = self.colors[i] if i < len(self.colors) else COLORS['BAR_DEFAULT']
            pygame.draw.rect(self.screen, color, (x, y, BAR_WIDTH, height))
            
            pygame.draw.rect(self.screen, (40, 40, 50), (x, y, BAR_WIDTH, height), 1)

        # Show Static Information
        info_text = (f"Comparisons: {self.comparisons}  Swaps: {self.swaps}  "
                     f"Steps: {self.step_count}  Speed: {self.speed} steps/sec")
        text_surface = self.font.render(info_text, True, COLORS['TEXT'])
        self.screen.blit(text_surface, (20, 20))

        # Show Status
        status = "Sorting..." if self.is_sorting and not self.is_paused else \
                 "Paused" if self.is_paused else "Idle"
        status_surface = self.big_font.render(status, True, COLORS['TEXT'])
        self.screen.blit(status_surface, (WIDTH - 200, 20))

        # Draw Button
        self.draw_buttons()

        pygame.display.flip()

    # Main Loop
    def run(self):
        running = True
        while running:
            
            if self.is_sorting and not self.is_paused:
                steps_to_run = max(1, self.speed // 30)   # Count of Steps per frame
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
    visualizer = BubbleSortVisualizer()
    visualizer.run()
