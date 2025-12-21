import pygame

class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value):
        self.x = x
        self.y = y
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.slider_width = 10
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, 10))
        
        knob_position = self.x + (self.value - self.min_value) * (self.width - self.slider_width) / (self.max_value - self.min_value)
        pygame.draw.rect(screen, (255, 0, 0), (knob_position, self.y - 5, self.slider_width, 20))
        
        font = pygame.font.Font(None, 30)
        value_text = font.render(f"Delay: {int(self.value)}ms", True, (255, 255, 255))
        screen.blit(value_text, (self.x + self.width + 10, self.y - 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if self.x <= mouse_x <= self.x + self.width and self.y - 5 <= mouse_y <= self.y + 15:
                    self.dragging = True
                    self.set_value(mouse_x)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.set_value(mouse_x)

    def set_value(self, mouse_x):
        new_value = self.min_value + (mouse_x - self.x) * (self.max_value - self.min_value) / self.width
        self.value = max(self.min_value, min(new_value, self.max_value))
