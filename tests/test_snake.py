import unittest
import pygame
import sys
import os

# Add the parent directory to the Python path to allow importing project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from snake import Snake

class TestSnake(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.segment_size = 20 # Corrected from grid_size
        self.snake = Snake(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            segment_size=self.segment_size, # Corrected
            color=(0,255,0), # Direct color
            initial_length=3
        )

    def test_initialization(self):
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, "RIGHT")
        # Check initial positions
        expected_head_x = self.screen_width // 2
        expected_head_y = self.screen_height // 2
        self.assertEqual(self.snake.body[0], (expected_head_x, expected_head_y))
        self.assertEqual(self.snake.body[1], (expected_head_x - self.segment_size, expected_head_y))

    def test_move_right(self):
        initial_head_pos_tuple = self.snake.body[0]
        self.snake.move()
        self.assertEqual(self.snake.body[0][0], initial_head_pos_tuple[0] + self.segment_size)
        self.assertEqual(self.snake.body[0][1], initial_head_pos_tuple[1])

    def test_change_direction_up(self):
        # Current head to compare after move
        # Snake starts moving right, so first segment is head.
        # After changing direction up, head is self.snake.body[0] still.
        self.snake.change_direction_up()
        self.assertEqual(self.snake.direction, "UP") # Direction should change immediately

        initial_head_pos_tuple = self.snake.body[0]
        self.snake.move() # First move in new direction
        self.assertEqual(self.snake.body[0][0], initial_head_pos_tuple[0])
        self.assertEqual(self.snake.body[0][1], initial_head_pos_tuple[1] - self.segment_size)


    def test_prevent_reverse_direction(self):
        self.snake.direction = "RIGHT" # Set explicitly
        self.snake.dx = self.segment_size; self.snake.dy = 0;
        self.snake.change_direction_left()
        self.assertEqual(self.snake.direction, "RIGHT")

        self.snake.direction = "LEFT"
        self.snake.dx = -self.segment_size; self.snake.dy = 0;
        self.snake.change_direction_right()
        self.assertEqual(self.snake.direction, "LEFT")

        self.snake.direction = "UP"
        self.snake.dx = 0; self.snake.dy = -self.segment_size;
        self.snake.change_direction_down()
        self.assertEqual(self.snake.direction, "UP")

        self.snake.direction = "DOWN"
        self.snake.dx = 0; self.snake.dy = self.segment_size;
        self.snake.change_direction_up()
        self.assertEqual(self.snake.direction, "DOWN")


    def test_grow(self):
        initial_length = len(self.snake.body)
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_self_collision(self):
        # Force a self-collision scenario: (head_x, head_y), (next_x, next_y), ..., (colliding_segment_x, colliding_segment_y)
        # Head is body[0]. It will collide with body[3] in this setup.
        self.snake.body = [
            (100, 100), # New head after a move
            (120, 100), # Prev head
            (100, 100), # This is where the new head will be, creating collision
            (80, 100)   # Tail
        ]
        # To make body[0] the head and simulate it just moved there
        self.snake.x, self.snake.y = self.snake.body[0]
        self.assertTrue(self.snake.check_collision())

    def test_wall_collision(self):
        # Left wall
        self.snake = Snake(self.screen_width, self.screen_height, self.segment_size, (0,255,0), 3)
        self.snake.body = [(0 - self.segment_size, self.screen_height // 2)] + self.snake.body[1:] # Move head out
        self.snake.x, self.snake.y = self.snake.body[0]
        self.assertTrue(self.snake.check_collision())

        # Right wall
        self.snake = Snake(self.screen_width, self.screen_height, self.segment_size, (0,255,0), 3)
        self.snake.body = [(self.screen_width, self.screen_height // 2)] + self.snake.body[1:]
        self.snake.x, self.snake.y = self.snake.body[0]
        self.assertTrue(self.snake.check_collision())

        # Top wall
        self.snake = Snake(self.screen_width, self.screen_height, self.segment_size, (0,255,0), 3)
        self.snake.body = [(self.screen_width // 2, 0 - self.segment_size)] + self.snake.body[1:]
        self.snake.x, self.snake.y = self.snake.body[0]
        self.assertTrue(self.snake.check_collision())

        # Bottom wall
        self.snake = Snake(self.screen_width, self.screen_height, self.segment_size, (0,255,0), 3)
        self.snake.body = [(self.screen_width // 2, self.screen_height)] + self.snake.body[1:]
        self.snake.x, self.snake.y = self.snake.body[0]
        self.assertTrue(self.snake.check_collision())

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
