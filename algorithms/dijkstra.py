from queue import PriorityQueue
import pygame

def dijkstra(draw, grid, start, end, check_events=None):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if check_events and check_events(event):
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            new_dist = dist[current] + 1
            
            if new_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = new_dist
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((new_dist, count, neighbor))
                    open_set_hash.add(neighbor)
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
