import pygame

class Snake:
    """
    Represents the snake in the game.
    Manages its movement, growth, drawing, and collision detection.
    """
    def __init__(self, screen_width, screen_height, segment_size=20, color=(0, 255, 0), initial_length=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.segment_size = segment_size
        self.color = color # Use provided color

        # Initial position: middle of the screen
        self.x = screen_width // 2
        self.y = screen_height // 2

        # Initial body: a list of (x, y) tuples. Head is at self.body[0]
        self.body = []
        for i in range(initial_length):
            self.body.append((self.x - i * segment_size, self.y))

        # Ensure head is at the correct starting x,y after body initialization
        if initial_length > 0:
            self.x, self.y = self.body[0]

        # Initial direction: right
        self.direction = "RIGHT"
        self.dx = segment_size
        self.dy = 0

        # self.speed = segment_size # Speed is effectively one segment per game tick (controlled by FPS)
        self.grow_counter = 0 # Counter for how many segments to grow

    def move(self):
        """Updates the snake's position and body segments."""
        # Update head logical position based on current direction
        # Note: self.x and self.y track the intended head position for the next move
        self.x += self.dx
        self.y += self.dy

        # Add new head to the beginning of the body list
        new_head = (self.x, self.y)
        self.body.insert(0, new_head)

        # If grow_counter is positive, don't remove tail (snake grows)
        if self.grow_counter > 0:
            self.grow_counter -= 1
        else:
            # Remove the last segment of the snake's body if not growing
            if len(self.body) > 1: # Ensure there's a tail to pop
                 self.body.pop()


    def grow(self):
        """Increments the grow counter, causing the snake to grow on the next move(s)."""
        self.grow_counter += 1

    def draw(self, screen):
        """Draws the snake on the given screen."""
        for segment_x, segment_y in self.body:
            pygame.draw.rect(
                screen, self.color, (segment_x, segment_y, self.segment_size, self.segment_size)
            )

    def check_collision(self):
        """
        Checks for collisions with the game boundaries or the snake's own body.
        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        if not self.body: # Should not happen in normal gameplay
            return False

        head_x, head_y = self.body[0]

        # Check wall collision
        if not (0 <= head_x < self.screen_width and 0 <= head_y < self.screen_height):
            return True

        # Check self-collision (head collides with any part of its body, excluding the head itself)
        for segment_x, segment_y in self.body[1:]:
            if head_x == segment_x and head_y == segment_y:
                return True
        return False

    def change_direction_up(self):
        """Changes the snake's direction to UP, if not currently moving DOWN."""
        if self.direction != "DOWN":
            self.direction = "UP"
            self.dx = 0
            self.dy = -self.segment_size

    def change_direction_down(self):
        """Changes the snake's direction to DOWN, if not currently moving UP."""
        if self.direction != "UP":
            self.direction = "DOWN"
            self.dx = 0
            self.dy = self.segment_size

    def change_direction_left(self):
        """Changes the snake's direction to LEFT, if not currently moving RIGHT."""
        if self.direction != "RIGHT":
            self.direction = "LEFT"
            self.dx = -self.segment_size
            self.dy = 0

    def change_direction_right(self):
        """Changes the snake's direction to RIGHT, if not currently moving LEFT."""
        if self.direction != "LEFT":
            self.direction = "RIGHT"
            self.dx = self.segment_size
            self.dy = 0
