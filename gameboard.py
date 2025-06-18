import pygame
from snake import Snake
from food import Food
from ui_manager import UIManager # Import UIManager

class GameBoard:
    """
    Orchestrates the game elements: Snake, Food, UI, and game logic.
    Manages game state, updates, drawing, and interactions between components.
    """
    def __init__(self, width, height, segment_size=20, theme=None, high_score=0,
                 initial_snake_length=3, points_per_food=10):
        self.width = width
        self.height = height
        self.segment_size = segment_size
        self.high_score = high_score
        self.theme = theme
        self.initial_snake_length = initial_snake_length
        self.points_per_food = points_per_food
        # snake_speed_increment_factor from config would be handled in main.py's game loop (FPS adjustment)

        if self.theme is None: # Fallback to a default theme if none provided
            # This default theme should ideally match the one in main.py's create_default_config()
            self.theme = {
                "name": "Default Fallback",
                "background_color": (0, 0, 0), "snake_color": (0, 255, 0),
                "food_color": (255, 0, 0), "text_color": (255, 255, 255),
                "font_name": None, "font_size_score": 36,
                "font_size_message": 48, "font_size_small_message": 36, # Matched to main's default
                "eat_sound": "assets/sounds/eat.wav",
                "game_over_sound": "assets/sounds/game_over.wav"
            }

        self.screen_color = self.theme["background_color"]

        # Initialize UIManager with theme
        self.ui_manager = UIManager(self.width, self.height, self.theme)

        # Pass themed colors and initial length to Snake
        self.snake = Snake(self.width, self.height, self.segment_size,
                           color=self.theme["snake_color"],
                           initial_length=self.initial_snake_length)
        self.food = Food(self.width, self.height, self.segment_size, color=self.theme["food_color"])
        self.food.spawn(self.snake.body) # Initial food spawn, avoiding the snake

        self.score = 0
        # self.high_score is already set from constructor
        self.game_over = False
        self.paused = False
        self.confirm_quit = False

        # Initialize sound
        try:
            pygame.mixer.init()
            self.eat_sound = pygame.mixer.Sound(self.theme["eat_sound"])
            self.game_over_sound = pygame.mixer.Sound(self.theme["game_over_sound"])
        except pygame.error as e:
            print(f"Warning: Could not load sound effects ({e}). Game will run without sound.")
            self.eat_sound = None
            self.game_over_sound = None

    def update(self):
        # Game logic should only run if not game over, not paused, and not confirming quit
        if not self.game_over and not self.paused and not self.confirm_quit:
            self.snake.move()

            # Check if snake eats food
            if self.food.is_eaten(self.snake.body[0], self.snake.body): # Pass snake body for smart respawn
                self.score += self.points_per_food # Use configured points
                self.snake.grow()
                # Speed increment logic would typically adjust FPS in main.py
                # e.g., main.current_fps *= (1 + main.snake_speed_increment_factor)
                if self.eat_sound:
                    self.eat_sound.play()

            # Check for collisions (self or wall)
            if self.snake.check_collision():
                self.game_over = True
                if self.game_over_sound:
                    self.game_over_sound.play()

    def draw(self, screen):
        # Fill the background
        screen.fill(self.screen_color)

        # Draw snake and food
        self.snake.draw(screen)
        self.food.draw(screen)

        # Draw score using UIManager
        self.ui_manager.draw_score(screen, self.score)

        # Display "Game Over" message using UIManager
        if self.game_over:
            self.ui_manager.draw_game_over_message(screen, self.score, self.high_score)
        elif self.paused: # Display "Paused" message if game is paused
            self.ui_manager.draw_pause_message(screen)
        elif self.confirm_quit: # Display "Quit?" confirmation
            self.ui_manager.draw_confirmation_dialog(screen, "Quit? (Y/N)")


    def reset_game(self):
        # Update high score if current score is higher before resetting score
        if self.score > self.high_score:
            self.high_score = self.score

        self.snake = Snake(self.width, self.height, self.segment_size,
                           color=self.theme["snake_color"],
                           initial_length=self.initial_snake_length)
        self.food = Food(self.width, self.height, self.segment_size, color=self.theme["food_color"])
        self.food.spawn(self.snake.body) # Ensure food spawns away from new snake

        self.score = 0 # Reset score after potentially updating high_score
        self.game_over = False
        self.paused = False
        self.confirm_quit = False
