# main.py
import pygame
from game.maze import Maze
from settings import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dynamic Maze Generation with Enhanced Features")

    maze = Maze(screen)
    maze.generate(0, 0)  # Generate the maze
    maze.visualize()  # Initially visualize the maze

    # Setup the event timers
    dynamic_update_event = pygame.USEREVENT + 1
    pygame.time.set_timer(dynamic_update_event, 1000)  # Update every second
    toggle_walls_event = pygame.USEREVENT + 2
    pygame.time.set_timer(toggle_walls_event, 3000)  # Toggle walls every 3 seconds

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If 'p' key is pressed
                    maze.find_path()  # Find and display the path
            elif event.type == dynamic_update_event:
                maze.update_obstacles()
                maze.visualize()
            elif event.type == toggle_walls_event:
                maze.update_walls()
                maze.visualize()

if __name__ == "__main__":
    main()
