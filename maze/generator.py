import random
from collections import deque
import pygame

def generate_maze(draw, grid, rows, complexity, check_events=None):
    # 1) Start with everything as a wall
    for row in grid:
        for node in row:
            node.make_barrier()

    start_x, start_y = 1, 1
    grid[start_x][start_y].reset()
    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    # 2) Classic DFS maze generation (perfect maze)
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

    # 3) Add complexity by breaking some walls to create loops
    #    `complexity` is just an arbitrary integer – tune as you like.
    #    You could also interpret it as a probability.
    wall_cells = []
    for i in range(1, rows - 1):
        for j in range(1, rows - 1):
            node = grid[i][j]
            if node.is_barrier():
                # Only consider interior walls (not outer border)
                wall_cells.append((i, j))

    # Example: try to open up to `complexity` walls (or fewer if not enough)
    openings = min(complexity, len(wall_cells))
    random.shuffle(wall_cells)

    opened = 0
    for (i, j) in wall_cells:
        if opened >= openings:
            break

        # Optionally: only break walls that connect two open regions
        # to ensure we create meaningful loops (not just dead pockets).
        # Here we do a simple heuristic: if at least two neighbors are open.
        open_neighbors = 0
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < rows and 0 <= nj < rows and not grid[ni][nj].is_barrier():
                open_neighbors += 1

        # Require at least 2 open neighbors to create a loop
        if open_neighbors >= 2:
            grid[i][j].reset()
            opened += 1

    # 4) Recompute neighbors now that walls and passages are finalized
    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    open_nodes = [node for row in grid for node in row if not node.is_barrier()]

    def bfs_farthest(start_node):
        visited_nodes = {start_node}
        queue = deque([(start_node, 0)])
        farthest = (start_node, 0)
        while queue:
            node, dist = queue.popleft()
            if dist > farthest[1]:
                farthest = (node, dist)
            for neighbor in node.neighbors:
                if neighbor not in visited_nodes and not neighbor.is_barrier():
                    visited_nodes.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return farthest[0]

    # Choose start/end as you already do
    random_node = random.choice(open_nodes)
    start = bfs_farthest(random_node)
    end = bfs_farthest(start)
    start.make_start()
    end.make_end()
    draw()
    return start, end