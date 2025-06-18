import unittest
import pygame
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gameboard import GameBoard # Updated import path
from src.ui_manager import UIManager # Updated import path
from src.snake import Snake # Updated import path
from src.food import Food # Updated import path

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        pygame.init()
        # Mock theme for GameBoard, matching structure used by GameBoard's fallback
        self.mock_theme = {
            "name": "Test Theme",
            "background_color": [0,0,0], "snake_color": [0,255,0],
            "food_color": [255,0,0], "text_color": [255,255,255],
            "font_name": None, "font_size_score": 36,
            "font_size_message": 48, "font_size_small_message": 36,
            "eat_sound": "assets/sounds/eat.wav", # Path, GameBoard handles loading
            "game_over_sound": "assets/sounds/game_over.wav"
        }
        self.screen_width = 800
        self.screen_height = 600
        self.segment_size = 20
        self.initial_snake_length = 3
        self.points_per_food = 10
        self.high_score = 0

        self.game_board = GameBoard(
            width=self.screen_width,
            height=self.screen_height,
            segment_size=self.segment_size,
            theme=self.mock_theme,
            high_score=self.high_score,
            initial_snake_length=self.initial_snake_length,
            points_per_food=self.points_per_food
        )
        # For UIManager calls within GameBoard.draw, a screen is needed.
        # We won't call draw directly in most logic tests, but UIManager is init'd.
        # self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))


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
        # Force snake's head to be on food's position
        self.game_board.snake.body[0] = self.game_board.food.position
        self.game_board.snake.x, self.game_board.snake.y = self.game_board.food.position

        self.game_board.update()

        self.assertEqual(self.game_board.score, initial_score + self.points_per_food)
        self.assertTrue(self.game_board.snake.grow_counter > 0)

    def test_game_over_self_collision(self):
        # Force self-collision: make head overlap with a body segment
        # (100,100), (120,100), (100,100) <- head (body[0]) will be (100,100)
        self.game_board.snake.body = [
            (100, 100),
            (120, 100),
            (100, 100)
        ]
        self.game_board.snake.x, self.game_board.snake.y = self.game_board.snake.body[0]

        self.game_board.update()
        self.assertTrue(self.game_board.game_over)

    def test_game_over_wall_collision(self):
        self.game_board.snake.body[0] = (-self.segment_size, self.screen_height // 2) # Move head out of bounds
        self.game_board.snake.x, self.game_board.snake.y = self.game_board.snake.body[0]

        self.game_board.update()
        self.assertTrue(self.game_board.game_over)

    def test_reset_game(self):
        self.game_board.score = 100
        self.game_board.game_over = True
        self.game_board.paused = True

        # Simulate high score update process that happens in reset_game
        if self.game_board.score > self.game_board.high_score:
            self.game_board.high_score = self.game_board.score
        current_high_score = self.game_board.high_score # Should be 100

        self.game_board.reset_game()

        self.assertEqual(self.game_board.score, 0)
        self.assertFalse(self.game_board.game_over)
        self.assertFalse(self.game_board.paused)
        self.assertEqual(len(self.game_board.snake.body), self.initial_snake_length)
        self.assertEqual(self.game_board.high_score, current_high_score) # High score should persist

    def test_high_score_update_on_reset_game(self):
        # Scenario 1: Current score beats high score
        self.game_board.score = 50
        self.game_board.high_score = 20
        self.game_board.reset_game() # reset_game updates high_score if current score is greater
        self.assertEqual(self.game_board.high_score, 50)

        # Scenario 2: Current score does not beat high score
        self.game_board.score = 10
        # high_score is already 50 from previous step in this test method instance
        self.game_board.reset_game()
        self.assertEqual(self.game_board.high_score, 50)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    # This allows running tests directly from this file
    # For discover, ensure this file is named test_*.py and in a package
    unittest.main()
