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

# COLORS
COLORS = {
    'BACKGROUND': (30, 30, 40),
    'BAR_DEFAULT': (100, 150, 255),
    'BAR_SWAPPING': (255, 80, 80),
    'BAR_SORTED': (80, 255, 80),
    'BAR_MERGING': (255, 220, 80),
    'BAR_COMPARING': (255, 150, 50),
    'TEXT': (255, 255, 255),
    'BUTTON': (60, 60, 80),
    'BUTTON_HOVER': (80, 80, 100),
    'BUTTON_TEXT': (220, 220, 220)
}


class MergeSortVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Merge Sort Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)

        # Array and parameters
        self.array = []
        self.colors = []
        self.steps = deque()          # Queue of steps to execute
        self.is_sorting = False
        self.is_paused = False
        self.speed = 30               # Count of Steps Per-Second
        self.comparisons = 0
        self.step_count = 0

        # Buttons
        self.buttons = []
        self.create_buttons()

        # Generate Random Array
        self.generate_array()

    def generate_array(self):
        # Generative Array Using Random Number
        self.array = [random.randint(10, MAX_VALUE) for _ in range(ARRAY_SIZE)]
        self.colors = [COLORS['BAR_DEFAULT'] for _ in range(ARRAY_SIZE)]
        self.comparisons = 0
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
            {'text': 'Start', 'x': x_start + btn_width + 20, 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Pause', 'x': x_start + 2 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False},
            {'text': 'Reset', 'x': x_start + 3 * (btn_width + 20), 'y': y_start, 'w': btn_width, 'h': btn_height, 'hover': False}
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
        # Managing button clicks
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

    # MAIN PART
    def start_sort(self):
        """Start sorting process ==> generate all steps and store in queue"""
        if self.is_sorting:
            return

        self.is_sorting = True
        self.is_paused = False
        self.comparisons = 0
        self.step_count = 0
        self.steps.clear()                       # Empty the previous queue

        # Generate steps using generator and add to queue
        generator = self.generate_steps(0, len(self.array) - 1)
        for step in generator:
            self.steps.append(step)              # Save each step in the queue

        # If no steps are produced (empty or single-element array), the sort is finished
        if not self.steps:
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def generate_steps(self, left, right):
        """Generate sorting steps recursively using yield"""
        if left >= right:
            return

        mid = (left + right) // 2

        # Divide Part
        yield ('divide', left, mid, right)

        # Sorting Left-Half
        yield from self.generate_steps(left, mid)

        # Sorting Right-Half
        yield from self.generate_steps(mid + 1, right)

        # Merging Two Half
        yield from self.merge_steps(left, mid, right)

    def merge_steps(self, left, mid, right):
        # Generating Merging Steps
        n1 = mid - left + 1
        n2 = right - mid

        left_arr = self.array[left:mid + 1]
        right_arr = self.array[mid + 1:right + 1]

        i = j = 0
        k = left

        # Highlight the area being merged
        merge_indices = list(range(left, right + 1))
        yield ('highlight', merge_indices, COLORS['BAR_MERGING'])

        while i < n1 and j < n2:
            self.comparisons += 1
            yield ('compare', left + i, mid + 1 + j)

            if left_arr[i] <= right_arr[j]:
                self.array[k] = left_arr[i]
                i += 1
            else:
                self.array[k] = right_arr[j]
                j += 1

            yield ('set_color', k, COLORS['BAR_SWAPPING'])
            yield ('update', k)
            k += 1

        while i < n1:
            self.array[k] = left_arr[i]
            yield ('set_color', k, COLORS['BAR_SWAPPING'])
            yield ('update', k)
            i += 1
            k += 1

        while j < n2:
            self.array[k] = right_arr[j]
            yield ('set_color', k, COLORS['BAR_SWAPPING'])
            yield ('update', k)
            j += 1
            k += 1

        # After merging ==> turn all elements in this section green
        yield ('highlight', list(range(left, right + 1)), COLORS['BAR_SORTED'])

    def run_sort(self):
        # Execute a step from the queue (called multiple times per frame)
        if not self.is_sorting or self.is_paused:
            return

        if self.steps:
            step = self.steps.popleft()
            self.step_count += 1
            self.apply_step(step)
        else:
            # All Steps Running
            self.is_sorting = False
            for i in range(len(self.array)):
                self.colors[i] = COLORS['BAR_SORTED']

    def apply_step(self, step):
        
        op = step[0]

        if op == 'divide':
            _, left, mid, right = step
            for i in range(left, mid + 1):
                self.colors[i] = (100, 180, 255)      # Light blue ==> For the Left-Half
            for i in range(mid + 1, right + 1):
                self.colors[i] = (180, 100, 255)      # Purple ==> For the Rihgt-Half
        elif op == 'highlight':
            _, indices, color = step
            for i in indices:
                self.colors[i] = color

        elif op == 'compare':
            _, idx1, idx2 = step
            # Reset unrelated colors
            for i in range(len(self.array)):
                if self.colors[i] not in (COLORS['BAR_SORTED'], COLORS['BAR_MERGING']):
                    self.colors[i] = COLORS['BAR_DEFAULT']
            self.colors[idx1] = COLORS['BAR_COMPARING']
            self.colors[idx2] = COLORS['BAR_COMPARING']

        elif op == 'set_color':
            _, idx, color = step
            self.colors[idx] = color

        elif op == 'update':
            _, idx = step
            pass  # For visual sync only

    # =========================================================

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

        # Show Information
        info_text = f"Comparisons: {self.comparisons}  Steps: {self.step_count}  Speed: {self.speed} steps/sec"
        text_surface = self.font.render(info_text, True, COLORS['TEXT'])
        self.screen.blit(text_surface, (20, 20))

        # Show Status
        status = "Sorting..." if self.is_sorting and not self.is_paused else \
                 "Paused" if self.is_paused else "Idle"
        status_surface = self.big_font.render(status, True, COLORS['TEXT'])
        self.screen.blit(status_surface, (WIDTH - 200, 20))

        # Draw Buttons
        self.draw_buttons()

        pygame.display.flip()

    def run(self):
        # Main Loop Program
        running = True
        while running:
            # Execute steps at a specific speed
            if self.is_sorting and not self.is_paused:
                steps_to_run = max(1, self.speed // 30)   # Count of Steps Per-Second
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
    visualizer = MergeSortVisualizer()
    visualizer.run()