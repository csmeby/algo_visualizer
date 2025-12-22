import pygame

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
ACCENT_COLOR = (64, 224, 208)

class UIPanel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_title = pygame.font.SysFont('arial', 30, bold=True)
        self.font_body = pygame.font.SysFont('arial', 18)
        self.font_small = pygame.font.SysFont('arial', 14)

    def draw(self, screen, algo_name, time_slider, complexity_slider):
        pygame.draw.rect(screen, BG_COLOR, (self.x, self.y, self.width, self.height))
        
        title_surf = self.font_title.render("Visualizer", True, ACCENT_COLOR)
        screen.blit(title_surf, (self.x + 20, self.y + 20))
        
        algo_label = self.font_body.render(f"Algorithm: {algo_name}", True, TEXT_COLOR)
        screen.blit(algo_label, (self.x + 20, self.y + 70))
        
        instructions = [
            "Controls:",
            "Space: Run",
            "M: Generate Maze",
            "C: Clear Grid",
            "",
            "1: BFS",
            "2: DFS",
            "3: Dijkstra",
            "4: A*",
            "5: Greedy",
            "",
            "Left Click: Draw",
            "Right Click: Erase"
        ]
        
        start_y = 360
        for line in instructions:
            text_surf = self.font_small.render(line, True, TEXT_COLOR)
            screen.blit(text_surf, (self.x + 20, start_y))
            start_y += 25
