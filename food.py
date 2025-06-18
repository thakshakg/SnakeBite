import pygame
import random

class Food:
    """
    Represents the food item in the game.
    Manages its position, drawing, and detection of being eaten.
    """
    def __init__(self, screen_width, screen_height, segment_size=20, color=(255, 0, 0)):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.segment_size = segment_size
        self.color = color # Use provided color
        self.position = (0, 0)  # Will be updated by spawn
        self.rect = pygame.Rect(0, 0, self.segment_size, self.segment_size)
        # Initial spawn is done by GameBoard after snake is created, to avoid overlap.
        # self.spawn() # Removed from here

    def spawn(self, snake_body=None):
        """
        Spawns the food at a random position on the grid, avoiding the snake's body if provided.
        Args:
            snake_body (list, optional): A list of (x, y) tuples representing the snake's segments.
                                         Defaults to None.
        """
        possible_positions = []
        for x in range(0, self.screen_width // self.segment_size):
            for y in range(0, self.screen_height // self.segment_size):
                pos = (x * self.segment_size, y * self.segment_size)
                if snake_body and pos in snake_body:
                    continue
                possible_positions.append(pos)

        if not possible_positions:
            # This should ideally not happen if the snake hasn't filled the whole screen
            # Fallback to any random position if no empty spot is found (very rare)
            print("Warning: No empty space to spawn food! Spawning randomly.")
            self.position = (random.randrange(0, self.screen_width // self.segment_size) * self.segment_size,
                             random.randrange(0, self.screen_height // self.segment_size) * self.segment_size)
        else:
            self.position = random.choice(possible_positions)

        self.rect.topleft = self.position

    def draw(self, screen):
        """Draws the food item on the given screen."""
        pygame.draw.rect(screen, self.color, self.rect)

    def is_eaten(self, snake_head_pos, snake_body_for_respawn=None):
        """
        Checks if the snake's head has collided with the food. If eaten, respawns the food.
        Args:
            snake_head_pos (tuple): The (x, y) coordinates of the snake's head.
            snake_body_for_respawn (list, optional): The snake's body, passed to spawn to avoid overlap.
        Returns:
            bool: True if eaten, False otherwise.
        """
        snake_head_rect = pygame.Rect(snake_head_pos[0], snake_head_pos[1], self.segment_size, self.segment_size)
        if self.rect.colliderect(snake_head_rect):
            self.spawn(snake_body=snake_body_for_respawn) # Pass snake body to avoid spawning on it
            return True
        return False
