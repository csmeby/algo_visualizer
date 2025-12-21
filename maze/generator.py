import random
from collections import deque
import pygame

def generate_maze(draw, grid, rows, check_events=None):
    for row in grid:
        for node in row:
            node.make_barrier()

    start_x, start_y = 1, 1
    grid[start_x][start_y].reset()

    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}

    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        if check_events:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None, None
                if check_events(event):
                    return None, None

        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows - 1 and 0 < ny < rows - 1:
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)

            wall_x = x + dx // 2
            wall_y = y + dy // 2

            grid[wall_x][wall_y].reset()
            grid[nx][ny].reset()

            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    open_nodes = [node for row in grid for node in row if not node.is_barrier()]

    def bfs_farthest(start_node):
        visited = {start_node}
        queue = deque([(start_node, 0)])
        farthest = (start_node, 0)

        while queue:
            node, dist = queue.popleft()
            if dist > farthest[1]:
                farthest = (node, dist)

            for neighbor in node.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return farthest[0]

    random_node = random.choice(open_nodes)
    start = bfs_farthest(random_node)
    end = bfs_farthest(start)

    start.make_start()
    end.make_end()

    draw()
    return start, end
