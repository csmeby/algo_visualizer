from queue import Queue
import pygame

def bfs(draw, grid, start, end, check_events=None):
    count = 0
    open_set = Queue()
    open_set.put(start)
    came_from = {}
    visited = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if check_events and check_events(event):
                return False

        current = open_set.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                open_set.put(neighbor)
                neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
