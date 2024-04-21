# game/maze.py
import numpy as np
import pygame
from .entities import Obstacle, DynamicWall
from settings import *

class Maze:
    def __init__(self, screen):
        self.screen = screen
        self.grid = np.zeros((MAZE_HEIGHT, MAZE_WIDTH), dtype=bool)
        self.obstacles = [
            Obstacle(10, 10, 'normal'),
            Obstacle(12, 12, 'normal'),
            Obstacle(30, 30, 'normal')
        ]
        self.dynamic_walls = [DynamicWall(12, 12), DynamicWall(18, 18)]

    def generate(self, x, y):
        self.grid[y][x] = True
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        np.random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and not self.grid[ny][nx]:
                self.grid[y + dy][x + dx] = True
                self.generate(nx, ny)

    def visualize(self):
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
