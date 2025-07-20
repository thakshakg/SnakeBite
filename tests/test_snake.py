import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.snake import Snake

class TestSnake(unittest.TestCase):

    def setUp(self):
        self.screen_width = 80
        self.screen_height = 24
        self.snake = Snake(
            width=self.screen_width,
            height=self.screen_height,
            initial_length=3
        )

    def test_initialization(self):
        self.assertEqual(len(self.snake.body), 3)
        self.assertIn(self.snake.direction, ['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def test_move(self):
        initial_head_pos = self.snake.body[0]
        self.snake.move()
        if self.snake.direction == 'UP':
            expected_head_pos = (initial_head_pos[0], initial_head_pos[1] - 1)
        elif self.snake.direction == 'DOWN':
            expected_head_pos = (initial_head_pos[0], initial_head_pos[1] + 1)
        elif self.snake.direction == 'LEFT':
            expected_head_pos = (initial_head_pos[0] - 1, initial_head_pos[1])
        elif self.snake.direction == 'RIGHT':
            expected_head_pos = (initial_head_pos[0] + 1, initial_head_pos[1])
        self.assertEqual(self.snake.body[0], expected_head_pos)

    def test_change_direction(self):
        self.snake.direction = 'UP'
        self.snake.change_direction_down()
        self.assertEqual(self.snake.direction, 'UP')

        self.snake.direction = 'DOWN'
        self.snake.change_direction_up()
        self.assertEqual(self.snake.direction, 'DOWN')

        self.snake.direction = 'LEFT'
        self.snake.change_direction_right()
        self.assertEqual(self.snake.direction, 'LEFT')

        self.snake.direction = 'RIGHT'
        self.snake.change_direction_left()
        self.assertEqual(self.snake.direction, 'RIGHT')

    def test_grow(self):
        initial_length = len(self.snake.body)
        self.snake.grow()
        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_self_collision(self):
        self.snake.body = [(10, 10), (11, 10), (10, 10)]
        self.assertTrue(self.snake.check_collision())

    def test_wall_collision(self):
        self.snake.body[0] = (-1, 10)
        self.assertTrue(self.snake.check_collision())

        self.snake.body[0] = (self.screen_width, 10)
        self.assertTrue(self.snake.check_collision())

        self.snake.body[0] = (10, -1)
        self.assertTrue(self.snake.check_collision())

        self.snake.body[0] = (10, self.screen_height)
        self.assertTrue(self.snake.check_collision())

if __name__ == '__main__':
    unittest.main()
