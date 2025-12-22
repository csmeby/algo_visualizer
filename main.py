import pygame
import sys
from grid import Grid
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.greedy import greedy
from maze.generator import generate_maze
from slider import Slider
from ui_panel import UIPanel
from button import Button


GRID_WIDTH = 800
SIDEBAR_WIDTH = 460
WINDOW_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
HEIGHT = 800
ROWS = 50

def get_clicked_pos(pos, rows, width):
    # Translate mouse coordinates to grid row/col
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
    pygame.display.set_caption("Algorithm Visualizer")
    
    grid_obj = Grid(ROWS, GRID_WIDTH)
    grid = grid_obj.grid
    
    ui_panel = UIPanel(GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    
    # time slider
    time_slider = Slider(GRID_WIDTH + 40, 150, 200, 1, 100, 10, "Delay", "ms") 

    # complexity slider
    complexity_slider = Slider(GRID_WIDTH + 40, 220, 200, 1, 250, 50, "Complexity", "")
    
    stop_button = Button(GRID_WIDTH + 40, 290, 200, 50, "STOP", (200, 50, 50), (255, 100, 100))

    start = None
    end = None
    
    current_algo = astar
    algo_name = "A*"
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        
        grid_obj.draw(screen)
        
        ui_panel.draw(screen, algo_name, time_slider, complexity_slider)
        time_slider.draw(screen)
        complexity_slider.draw(screen)
        stop_button.draw(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            time_slider.handle_event(event)
            complexity_slider.handle_event(event)
            stop_button.handle_event(event)

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                
                # Prevent drawing outside grid area
                if pos[0] < GRID_WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if row < ROWS and col < ROWS:
                        node = grid[row][col]
                        if not start and node != end:
                            start = node
                            start.make_start()
                        elif not end and node != start:
                            end = node
                            end.make_end()
                        elif node != end and node != start:
                            node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if row < ROWS and col < ROWS:
                        node = grid[row][col]
                        node.reset()
                        if node == start:
                            start = None
                        elif node == end:
                            end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    def check_events(event):
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if stop_button.is_clicked(event.pos):
                                return True
                        time_slider.handle_event(event)
                        complexity_slider.handle_event(event)
                        # Hover effect needs event handling even during algo run
                        stop_button.handle_event(event) 
                        return False

                    def draw_with_delay():
                        grid_obj.draw(screen)
                        ui_panel.draw(screen, algo_name, time_slider, complexity_slider)
                        time_slider.draw(screen)
                        complexity_slider.draw(screen)
                        stop_button.draw(screen)
                        pygame.display.flip()
                        pygame.time.delay(int(time_slider.value))

                    current_algo(draw_with_delay, grid, start, end, check_events)

                if event.key == pygame.K_m:
                    start = None
                    end = None
                    
                    def check_events(event):
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if stop_button.is_clicked(event.pos):
                                return True
                        complexity_slider.handle_event(event)
                        return False

                    def draw_maze_step():
                        grid_obj.draw(screen)
                        ui_panel.draw(screen, algo_name, time_slider, complexity_slider)
                        time_slider.draw(screen)
                        complexity_slider.draw(screen)
                        stop_button.draw(screen)
                        pygame.display.flip()
                        # No delay for maze generation steps to keep it purely visual but fast
                    
                    complexity = int(complexity_slider.value)
                    start, end = generate_maze(draw_maze_step, grid, ROWS, complexity, check_events)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid_obj = Grid(ROWS, GRID_WIDTH)
                    grid = grid_obj.grid

                # Algorithm Selection
                if event.key == pygame.K_1:
                    current_algo = bfs
                    algo_name = "BFS"
                elif event.key == pygame.K_2:
                    current_algo = dfs
                    algo_name = "DFS"
                elif event.key == pygame.K_3:
                    current_algo = dijkstra
                    algo_name = "Dijkstra"
                elif event.key == pygame.K_4:
                    current_algo = astar
                    algo_name = "A*"
                elif event.key == pygame.K_5:
                    current_algo = greedy
                    algo_name = "Greedy"

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
