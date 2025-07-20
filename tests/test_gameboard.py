import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gameboard import GameBoard
from src.snake import Snake
from src.food import Food
from src.ui_manager import UIManager

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.screen_width = 80
        self.screen_height = 24
        self.initial_snake_length = 3
        self.points_per_food = 10
        self.high_score = 0

        self.game_board = GameBoard(
            width=self.screen_width,
            height=self.screen_height,
            high_score=self.high_score,
            initial_snake_length=self.initial_snake_length,
            points_per_food=self.points_per_food
        )

    def test_initialization(self):
        self.assertEqual(self.game_board.score, 0)
        self.assertFalse(self.game_board.game_over)
        self.assertFalse(self.game_board.paused)
        self.assertIsInstance(self.game_board.snake, Snake)
        self.assertEqual(len(self.game_board.snake.body), self.initial_snake_length)
        self.assertIsInstance(self.game_board.food, Food)
        self.assertIsInstance(self.game_board.ui_manager, UIManager)

    def test_food_eaten_score_increase_and_growth(self):
        initial_score = self.game_board.score
        initial_length = len(self.game_board.snake.body)
        self.game_board.snake.body[0] = self.game_board.food.position

        self.game_board.update()

        self.assertEqual(self.game_board.score, initial_score + self.points_per_food)
        self.assertEqual(len(self.game_board.snake.body), initial_length + 1)

    def test_game_over_self_collision(self):
        self.game_board.snake.body = [(10, 10), (11, 10), (10, 10)]
        self.game_board.update()
        self.assertTrue(self.game_board.game_over)

    def test_game_over_wall_collision(self):
        self.game_board.snake.body[0] = (-1, 10)
        self.game_board.update()
        self.assertTrue(self.game_board.game_over)

    def test_reset_game(self):
        self.game_board.score = 100
        self.game_board.game_over = True
        self.game_board.paused = True

        if self.game_board.score > self.game_board.high_score:
            self.game_board.high_score = self.game_board.score
        current_high_score = self.game_board.high_score

        self.game_board.reset_game()

        self.assertEqual(self.game_board.score, 0)
        self.assertFalse(self.game_board.game_over)
        self.assertFalse(self.game_board.paused)
        self.assertEqual(len(self.game_board.snake.body), self.initial_snake_length)
        self.assertEqual(self.game_board.high_score, current_high_score)

    def test_high_score_update_on_reset_game(self):
        self.game_board.score = 50
        self.game_board.high_score = 20
        self.game_board.reset_game()
        self.assertEqual(self.game_board.high_score, 50)

        self.game_board.score = 10
        self.game_board.reset_game()
        self.assertEqual(self.game_board.high_score, 50)

if __name__ == '__main__':
    unittest.main()
