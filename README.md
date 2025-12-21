# Algorithm Visualizer

A powerful, interactive desktop application to visualize pathfinding algorithms in action. Built with **Python** and **Pygame**, this tool demonstrates how various search algorithms explore a grid to find the shortest path between two points.

## Features

-   **Pathfinding Algorithms**: Visualize the execution of popular algorithms:
    -   **A* Search**: Weighted, guarantees shortest path (usually fastest).
    -   **Dijkstra's Algorithm**: Weighted, guarantees shortest path.
    -   **Breadth-First Search (BFS)**: Unweighted, guarantees shortest path.
    -   **Depth-First Search (DFS)**: Unweighted, does not guarantee shortest path.
-   **Maze Generation**: Automatically generate complex mazes using a **Recursive Backtracker** algorithm.
-   **Interactive Grid**: Draw your own walls, move start/end nodes, and clear the grid.
-   **Speed Control**: Adjust the visualization speed in real-time with a slider.
-   **Real-time Stats**: See the algorithm explore nodes (Green) and finalize paths (Red) and the best path (Purple).

## Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/csmeby/algo_visualizer.git
    cd algo_visualizer
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

Run the application:
```bash
python main.py
```

### Controls

| Key / Action | Description |
| :--- | :--- |
| **Left Click** | Place **Start** (Orange), **End** (Turquoise), or **Walls** (Black) |
| **Right Click** | Remove nodes (Erase) |
| **Space** | **Run** the selected algorithm |
| **1** | Select **BFS** |
| **2** | Select **DFS** |
| **3** | Select **Dijkstra** |
| **4** | Select **A*** (Default) |
| **M** | Generate a **Maze** |
| **C** | **Clear** the grid |
| **Sidebar "STOP"** | Stop the current running algorithm |
| **Slider** | Drag to adjust animation delay (Speed) |

## Algorithms Explained

-   **A\* (A-Star)**: Uses heuristics to estimate cost to target, prioritizing nodes that seem promising. It is generally the best pathfinding algorithm.
-   **Dijkstra**: Expands in all directions equally, guaranteeing the shortest path but potential exploring unnecessary nodes.
-   **BFS**: Explores layer by layer. Great for unweighted graphs.
-   **DFS**: Explores as far as possible along each branch before backtracking. Can be fast but often produces unoptimized paths.