import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.food import Food

class TestFood(unittest.TestCase):

    def setUp(self):
        self.screen_width = 80
        self.screen_height = 24
        self.food = Food(
            width=self.screen_width,
            height=self.screen_height,
        )
        self.snake_body = [(10, 10), (10, 11), (10, 12)]

    def test_initialization_and_spawn(self):
        self.assertTrue(0 <= self.food.position[0] < self.screen_width)
        self.assertTrue(0 <= self.food.position[1] < self.screen_height)

    def test_spawn_avoids_snake(self):
        # Create a snake body that occupies a small portion of the screen
        snake_body = [(x, y) for x in range(5) for y in range(5)]

        # Spawn food multiple times and check it doesn't spawn in the snake body
        for _ in range(100):
            self.food.spawn(snake_body=snake_body)
            self.assertNotIn(self.food.position, snake_body)

    def test_is_eaten(self):
        snake_head_pos = self.food.position
        initial_food_pos = self.food.position
        self.assertTrue(self.food.is_eaten(snake_head_pos, self.snake_body))
        self.assertNotEqual(self.food.position, initial_food_pos)

        snake_head_far = (0, 0)
        if self.food.position == snake_head_far:
            self.food.spawn(snake_body=[snake_head_far])

        self.assertFalse(self.food.is_eaten(snake_head_far, self.snake_body))

if __name__ == '__main__':
    unittest.main()
