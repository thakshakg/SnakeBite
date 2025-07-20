from .snake import Snake
from .food import Food
from .ui_manager import UIManager

class GameBoard:
    def __init__(self, width, height, high_score=0,
                 initial_snake_length=3, points_per_food=10):
        self.width = width
        self.height = height
        self.high_score = high_score
        self.initial_snake_length = initial_snake_length
        self.points_per_food = points_per_food

        self.ui_manager = UIManager(self.width, self.height)
        self.snake = Snake(self.width, self.height, initial_length=self.initial_snake_length)
        self.food = Food(self.width, self.height)
        self.food.spawn(self.snake.body)

        self.score = 0
        self.game_over = False
        self.paused = False
        self.confirm_quit = False

    def update(self):
        if not self.game_over and not self.paused and not self.confirm_quit:
            self.snake.move()

            if self.food.is_eaten(self.snake.body[0], self.snake.body):
                self.score += self.points_per_food
                self.snake.grow()

            if self.snake.check_collision():
                self.game_over = True

    def draw_to_string(self):
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.snake.draw_to_string(board)
        self.food.draw_to_string(board)

        for row in board:
            print(''.join(row))

        self.ui_manager.draw_score_to_string(self.score)

        if self.game_over:
            self.ui_manager.draw_game_over_message_to_string(self.score, self.high_score)
        elif self.paused:
            self.ui_manager.draw_pause_message_to_string()
        elif self.confirm_quit:
            self.ui_manager.draw_confirmation_dialog_to_string("Quit? (y/n)")

    def reset_game(self):
        if self.score > self.high_score:
            self.high_score = self.score

        self.snake = Snake(self.width, self.height, initial_length=self.initial_snake_length)
        self.food = Food(self.width, self.height)
        self.food.spawn(self.snake.body)

        self.score = 0
        self.game_over = False
        self.paused = False
        self.confirm_quit = False
