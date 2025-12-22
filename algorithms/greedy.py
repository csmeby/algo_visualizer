from queue import PriorityQueue
import pygame

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def greedy(draw, grid, start, end, check_events=None):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    visited = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if check_events and check_events(event):
                return False

        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                priority = h(neighbor.get_pos(), end.get_pos())
                count += 1
                open_set.put((priority, count, neighbor))
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