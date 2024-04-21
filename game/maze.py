# game/maze.py
from .entities import Obstacle, DynamicWall
# game/maze.py
import numpy as np
import pygame
from .pathfinding import a_star_search, heuristic, PriorityQueue
from settings import *

class Maze:
    def __init__(self, screen):
        self.screen = screen
        self.grid = np.zeros((MAZE_HEIGHT, MAZE_WIDTH), dtype=bool)
        self.obstacles = [
            Obstacle(10, 10, 'normal'), 
            Obstacle(15, 15, 'fast'), 
            Obstacle(20, 20, 'normal')
        ]
        self.dynamic_walls = [DynamicWall(12, 12), DynamicWall(18, 18)]
        self.start = (1, 1)  # Start position for pathfinding
        self.goal = (MAZE_WIDTH-2, MAZE_HEIGHT-2)  # Goal position

    def generate(self, x, y):
        # Recursive maze generation with random path creation
        self.grid[y][x] = True
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        np.random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and not self.grid[ny][nx]:
                self.grid[y + dy][x + dx] = True
                self.generate(nx, ny)

    def neighbors(self, node):
        # Check the four possible movements (up, down, left, right)
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions: down, right, up, left
        result = []
        x, y = node
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and self.grid[ny][nx]:
                result.append((nx, ny))
        return result

    def cost(self, from_node, to_node):
        # Assuming uniform cost for simplicity
        return 1

    def find_path(self):
        # Finds a path from the start to the goal using A* algorithm
        came_from, cost_so_far = a_star_search(self, self.start, self.goal)
        self.draw_path(came_from)

    def draw_path(self, came_from):
        # Draw the path from start to goal
        current = self.goal
        while current != self.start:
            x, y = current
            pygame.draw.rect(self.screen, (0, 255, 0), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            current = came_from.get(current)
            if current is None:
                break
        pygame.display.flip()

    def visualize(self):
        # Draws the maze, obstacles, and dynamic walls
        self.screen.fill(WHITE)
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, YELLOW, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, RED, (obstacle.x * GRID_SIZE, obstacle.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for wall in self.dynamic_walls:
            if wall.active:
                pygame.draw.rect(self.screen, GRAY, (wall.x * GRID_SIZE, wall.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move(self.grid, self.obstacles)

    def update_walls(self):
        for wall in self.dynamic_walls:
            wall.toggle()
