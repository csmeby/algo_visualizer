import pygame
import sys
import random
import time
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
from algorithms.bubble_sort import bubbleSort
from algorithms.insertion_sort import insertionSort
from algorithms.selection_sort import selectionSort
from algorithms.quick_sort import quickSort
from algorithms.radix_sort import radixSort
from algorithms.merge_sort import mergeSort

GRID_WIDTH = 800
SIDEBAR_WIDTH = 460
WINDOW_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH
HEIGHT = 800
ROWS = 50

WHITE = (245, 245, 245)
BLUE = (0, 123, 255)
LIGHT_GRAY = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def run_pathfinding(screen):
    pygame.display.set_caption("Pathfinding Visualizer")
    grid_obj = Grid(ROWS, GRID_WIDTH)
    grid = grid_obj.grid
    
    ui_panel = UIPanel(GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    
    time_slider = Slider(GRID_WIDTH + 40, 150, 200, 1, 100, 10, "Delay", "ms") 
    complexity_slider = Slider(GRID_WIDTH + 40, 220, 200, 1, 250, 50, "Complexity", "")
    stop_button = Button(GRID_WIDTH + 40, 290, 200, 50, "STOP", (200, 50, 50), (255, 100, 100))

    start = None
    end = None
    
    current_algo = astar
    algo_name = "A*"
    
    running = True
    while running:
        screen.fill(WHITE)
        
        grid_obj.draw(screen)
        
        ui_panel.draw(screen, algo_name, time_slider, complexity_slider)
        time_slider.draw(screen)
        complexity_slider.draw(screen)
        stop_button.draw(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            time_slider.handle_event(event)
            complexity_slider.handle_event(event)
            stop_button.handle_event(event)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
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

            elif pygame.mouse.get_pressed()[2]:
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
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if stop_button.is_clicked(event.pos):
                                return True
                        time_slider.handle_event(event)
                        complexity_slider.handle_event(event)
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
                    
                    complexity = int(complexity_slider.value)
                    start, end = generate_maze(draw_maze_step, grid, ROWS, complexity, check_events)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid_obj = Grid(ROWS, GRID_WIDTH)
                    grid = grid_obj.grid

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

def run_sorting(screen):
    pygame.display.set_caption("Sorting Visualizer")
    
    
    ui_panel = UIPanel(GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    time_slider = Slider(GRID_WIDTH + 40, 150, 200, 1, 100, 10, "Delay", "ms")
    complexity_slider = Slider(GRID_WIDTH + 40, 220, 200, 10, 100, 50, "Array Size", "")
    stop_button = Button(GRID_WIDTH + 40, 290, 200, 50, "STOP", (200, 50, 50), (255, 100, 100))

    n = int(complexity_slider.value)
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    
    algo_name = "Bubble Sort"
    current_algo = bubbleSort
    
    is_sorted = False

    def draw_sorting(arr, compare_indices=[], green_indices=[], end=False):
        screen.fill(WHITE)
        
        if len(arr) > 0:
            bar_width = (GRID_WIDTH // len(arr)) + 1 

            bar_width = GRID_WIDTH // len(arr) 
            if bar_width < 1: bar_width = 1

            max_val = max(arr) if arr else 1
            max_height = HEIGHT - 50

            for i, value in enumerate(arr):
                x = i * bar_width
                height = (value / max_val) * max_height
                y = HEIGHT - height
                
                color = BLUE
                if i in green_indices:
                    color = GREEN
                elif i in compare_indices:
                    color = RED
                

                pygame.draw.rect(screen, color, (x, y, bar_width, height))
        
        ui_panel.draw(screen, algo_name, time_slider, complexity_slider, "sorting")
        time_slider.draw(screen)
        complexity_slider.draw(screen)
        stop_button.draw(screen)
        
        pygame.display.flip()

    running = True
    while running:
        current_green = range(len(arr)) if is_sorted else []
        draw_sorting(arr, green_indices=current_green)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            time_slider.handle_event(event)
            if complexity_slider.handle_event(event):
                 n = int(complexity_slider.value)
                 arr = list(range(1, n + 1))
                 random.shuffle(arr)
                 is_sorted = False

            stop_button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and stop_button.is_clicked(event.pos):
                 n = int(complexity_slider.value)
                 arr = list(range(1, n + 1))
                 random.shuffle(arr)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                     n = int(complexity_slider.value)
                     arr = list(range(1, n + 1))
                     random.shuffle(arr)
                     is_sorted = False
                
                if event.key == pygame.K_SPACE and not is_sorted:
                    delay = time_slider.value / 1000.0
                    
                    def draw_wrapper(arr, compare_indices, end=False):
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                sys.exit()
                            if e.type == pygame.MOUSEBUTTONDOWN and stop_button.is_clicked(e.pos):
                                raise Exception("StopAlgorithm")

                        if end:
                           # animate green
                            nonlocal is_sorted
                            is_sorted = True
                            for i in range(len(arr)):
                                 # check for stop/quit during animation to be responsive
                                for e in pygame.event.get():
                                    if e.type == pygame.QUIT:
                                        sys.exit()
                                    if e.type == pygame.MOUSEBUTTONDOWN and stop_button.is_clicked(e.pos):
                                        is_sorted = False
                                        return # break animation

                                draw_sorting(arr, green_indices=range(i + 1))
                                pygame.time.delay(20) # fast animation delay
                        else:
                            draw_sorting(arr, compare_indices, end=end)

                    try:
                        current_algo(arr, draw_wrapper, delay)
                    except Exception as e:
                        if str(e) == "StopAlgorithm":
                            pass
                        else:
                            pass

                if event.key == pygame.K_1:
                    current_algo = bubbleSort
                    algo_name = "Bubble Sort"
                elif event.key == pygame.K_2:
                    current_algo = insertionSort
                    algo_name = "Insertion Sort"
                elif event.key == pygame.K_3:
                    current_algo = selectionSort
                    algo_name = "Selection Sort"
                elif event.key == pygame.K_4:
                    current_algo = quickSort
                    algo_name = "Quick Sort"
                elif event.key == pygame.K_5:
                    current_algo = radixSort
                    algo_name = "Radix Sort"
                elif event.key == pygame.K_6:
                    current_algo = mergeSort
                    algo_name = "Merge Sort"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
    pygame.display.set_caption("Algorithm Visualizer")
    
    pathfinding_btn = Button(WINDOW_WIDTH//2 - 150, 300, 300, 60, "Searching Algorithms", BLUE, LIGHT_GRAY, (0,0,0))
    sorting_btn = Button(WINDOW_WIDTH//2 - 150, 400, 300, 60, "Sorting Algorithms", BLUE, LIGHT_GRAY, (0,0,0))
    
    while True:
        screen.fill(WHITE)
        
        pathfinding_btn.draw(screen)
        sorting_btn.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            pathfinding_btn.handle_event(event)
            sorting_btn.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pathfinding_btn.is_clicked(event.pos):
                    run_pathfinding(screen)
                    pygame.display.set_caption("Algorithm Visualizer")
                elif sorting_btn.is_clicked(event.pos):
                    run_sorting(screen)
                    pygame.display.set_caption("Algorithm Visualizer")
                    
        pygame.display.flip()

if __name__ == "__main__":
    main()
