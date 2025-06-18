import unittest
import pygame
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from food import Food
# Snake is not directly used but its body structure (list of tuples) is relevant for spawn testing
# from snake import Snake

class TestFood(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.segment_size = 20 # Corrected from grid_size
        self.food = Food(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            segment_size=self.segment_size, # Corrected
            color=(255,0,0) # Direct color
        )
        # Food is not spawned in constructor, so spawn it here for most tests
        self.food.spawn()

        # Mock snake body for spawn testing (list of (x,y) tuples)
        self.snake_body_tuples = [
            (0,0),
            (self.segment_size,0)
        ]

    def test_initialization_and_spawn(self):
        # Test that spawn sets a valid position
        self.assertIsInstance(self.food.rect, pygame.Rect)
        self.assertEqual(self.food.position, self.food.rect.topleft)
        self.assertTrue(0 <= self.food.position[0] < self.screen_width)
        self.assertTrue(0 <= self.food.position[1] < self.screen_height)
        self.assertEqual(self.food.position[0] % self.segment_size, 0)
        self.assertEqual(self.food.position[1] % self.segment_size, 0)

    def test_spawn_avoids_snake(self):
        # Create a snake body that fills almost the entire screen
        full_snake_body_tuples = []
        test_spot_x = self.segment_size * 5
        test_spot_y = self.segment_size * 5

        for x_idx in range(self.screen_width // self.segment_size):
            for y_idx in range(self.screen_height // self.segment_size):
                x_coord = x_idx * self.segment_size
                y_coord = y_idx * self.segment_size
                if x_coord == test_spot_x and y_coord == test_spot_y:
                    continue # Leave one spot open
                full_snake_body_tuples.append((x_coord, y_coord))

        self.food.spawn(snake_body=full_snake_body_tuples)
        # Food should spawn in the only free spot
        self.assertEqual(self.food.position, (test_spot_x, test_spot_y))
        self.assertEqual(self.food.rect.topleft, (test_spot_x, test_spot_y))

    def test_is_eaten(self):
        # Position snake head on food
        snake_head_pos_tuple = self.food.position

        # Check if eaten - this will also call spawn again
        initial_food_pos = self.food.position
        self.assertTrue(self.food.is_eaten(snake_head_pos_tuple, self.snake_body_tuples))
        # After being eaten, food should have respawned to a new location
        self.assertNotEqual(self.food.position, initial_food_pos)

        # Test with snake head far from food
        snake_head_far_tuple = (0,0)
        # Ensure current food position is not (0,0) before this part of the test
        if self.food.position == snake_head_far_tuple:
            self.food.spawn(snake_body=[snake_head_far_tuple]) # Ensure it's different

        self.assertFalse(self.food.is_eaten(snake_head_far_tuple, self.snake_body_tuples))

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
