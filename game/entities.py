# game/entities.py
import random

class Obstacle:
    def __init__(self, x, y, type='normal'):
        self.x = x
        self.y = y
        self.type = type

    def move(self, grid, obstacles):
        # print(f"Obstacle at ({self.x}, {self.y}) attempting to move. Type: {self.type}")
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        # if self.type == 'fast':
        #     directions.extend([(4, 0), (-4, 0), (0, 4), (0, -4)])
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx]:
                if not any(obst.x == nx and obst.y == ny for obst in obstacles if obst != self):
                    self.x, self.y = nx, ny
                    # print(f"Moved to ({self.x}, {self.y})")
                    return
        # print("No valid move found.")

class DynamicWall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def toggle(self):
        self.active = not self.active
        print(f"Wall at ({self.x}, {self.y}) toggled to {'active' if self.active else 'inactive'}.")
