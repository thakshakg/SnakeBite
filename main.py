import pygame
import json # Import json module
from gameboard import GameBoard # Import GameBoard

CONFIG_FILE = "config.json" # Filepath for the configuration file

def create_default_config():
    """
    Creates a dictionary containing the default configuration settings for the game.
    These settings are used if the config file is missing or corrupted.
    Returns:
        dict: The default configuration.
    """
    return {
        "screen_width": 800,
        "screen_height": 600,
        "fps": 10, # Frames per second, also initial snake speed
        "high_score": 0,
        "initial_snake_length": 3,
        "points_per_food": 10,
        "snake_speed_increment_factor": 0.0, # Factor to increase FPS by per food (0.0 = no increase)
        "theme": { # Visual theme settings
            "name": "Default",
            "background_color": [0, 0, 0], # Black
            "snake_color": [0, 255, 0],   # Green
            "food_color": [255, 0, 0],    # Red
            "text_color": [255, 255, 255], # White
            "font_name": None,            # Pygame's default system font
            "font_size_score": 36,
            "font_size_message": 48,
            "font_size_small_message": 36,
            "eat_sound": "assets/sounds/eat.wav",       # Path to sound for eating food
            "game_over_sound": "assets/sounds/game_over.wav" # Path to sound for game over
        }
    }

def load_config():
    """
    Loads game configuration from CONFIG_FILE.
    If the file is not found or is corrupted, it creates and returns a default configuration,
    and saves this default configuration for future use.
    Returns:
        dict: The loaded (or default) game configuration.
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
            # Validate and fill missing keys with defaults to ensure robustness
            default_config_template = create_default_config()
            for key, default_value in default_config_template.items():
                if key not in config_data:
                    print(f"Warning: Config key '{key}' missing. Using default value.")
                    config_data[key] = default_value
                elif isinstance(default_value, dict): # For nested dicts like 'theme'
                    for sub_key, sub_default_value in default_value.items():
                        if sub_key not in config_data[key]:
                             print(f"Warning: Theme key '{sub_key}' missing. Using default value.")
                             config_data[key][sub_key] = sub_default_value
            return config_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Error loading {CONFIG_FILE} ({e}). Creating and using default config.")
        default_config = create_default_config()
        save_config(default_config) # Attempt to save the default config for next launch
        return default_config

def save_config(config_data):
    """
    Saves the given configuration data to CONFIG_FILE.
    Args:
        config_data (dict): The configuration dictionary to save.
    """
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2) # indent=2 for pretty printing
    except IOError as e:
        print(f"Error: Could not save config to {CONFIG_FILE} ({e}).")

# --- Main Program Start ---
def main():
    """
    Main function to initialize and run the Snake game.
    """
    pygame.init() # Initialize all imported Pygame modules

    # Load configuration
    config = load_config()

    # Extract settings from config with fallbacks if any top-level key is unexpectedly missing
    screen_width = config.get("screen_width", 800)
    screen_height = config.get("screen_height", 600)
    base_fps = config.get("fps", 10)
    current_fps = base_fps # FPS can change if speed increment is implemented (not fully in this version)
    # snake_speed_increment_factor = config.get("snake_speed_increment_factor", 0.0) # For future use

    theme = config.get("theme", create_default_config()["theme"]) # Fallback for whole theme
    high_score = config.get("high_score", 0)
    initial_snake_length = config.get("initial_snake_length", 3)
    points_per_food = config.get("points_per_food", 10)
    segment_size = 20 # Could be moved to config if more granular control is needed

    # Create the game screen (display surface)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game") # Set the window title

    # Create GameBoard instance, passing all necessary settings
    game_board = GameBoard(
        screen_width, screen_height, segment_size,
        theme=theme,
        high_score=high_score,
        initial_snake_length=initial_snake_length,
        points_per_food=points_per_food
    )

    clock = pygame.time.Clock() # Pygame clock to control FPS
    running = True # Main game loop flag

    # --- Main Game Loop ---
    while running:
        # Event Handling: Process all events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # User clicked the window close button
                if not game_board.confirm_quit:
                    game_board.confirm_quit = True
                    game_board.paused = False # Ensure pause is not active during quit confirm

            if event.type == pygame.KEYDOWN: # A key was pressed
                # Handle inputs for the quit confirmation dialog
                if game_board.confirm_quit:
                    if event.key == pygame.K_y: # 'Y' to confirm quit
                        running = False
                    elif event.key == pygame.K_n: # 'N' to cancel quit
                        game_board.confirm_quit = False

                # Handle Escape key for pausing or canceling quit
                elif event.key == pygame.K_ESCAPE:
                    if game_board.paused:
                        game_board.paused = False # Unpause
                    elif not game_board.game_over and not game_board.confirm_quit:
                        game_board.paused = True # Pause active game
                    elif game_board.confirm_quit: # If in quit confirmation, ESC cancels it
                        game_board.confirm_quit = False

                # Handle Spacebar for pause/unpause (alternative to ESC)
                elif event.key == pygame.K_SPACE:
                    if not game_board.game_over and not game_board.confirm_quit:
                        game_board.paused = not game_board.paused

                # Handle "R" for Resetting the game when game is over
                elif event.key == pygame.K_r:
                    if game_board.game_over:
                        game_board.reset_game()
                        current_fps = base_fps # Reset FPS if it was changed

                # Handle Arrow Keys for Snake Movement (only if game is active)
                elif not game_board.paused and not game_board.game_over and not game_board.confirm_quit:
                    if event.key == pygame.K_UP:
                        game_board.snake.change_direction_up()
                    elif event.key == pygame.K_DOWN:
                        game_board.snake.change_direction_down()
                    elif event.key == pygame.K_LEFT:
                        game_board.snake.change_direction_left()
                    elif event.key == pygame.K_RIGHT:
                        game_board.snake.change_direction_right()

        # --- Game Logic Update ---
        # GameBoard's update method handles its internal state (snake movement, collisions, food)
        # based on its current flags (paused, game_over, confirm_quit).
        game_board.update()
        # Example of speed increment (conceptual, needs careful integration with game_board.update)
        # if game_board.just_ate_food and snake_speed_increment_factor > 0:
        # current_fps += base_fps * snake_speed_increment_factor
        # game_board.just_ate_food = False # Reset flag in GameBoard

        # --- Drawing ---
        # GameBoard's draw method handles rendering all game elements based on its state.
        game_board.draw(screen)
        pygame.display.flip() # Update the full display surface to the screen

        # --- Frame Rate Control ---
        clock.tick(current_fps) # Limit FPS

    # --- End of Game Loop ---

    # Update high score in config before quitting
    config["high_score"] = game_board.high_score
    # Potentially save other settings if they were changed during gameplay, e.g., config["fps"] = base_fps
    save_config(config)

    pygame.quit() # Uninitialize all Pygame modules

if __name__ == '__main__':
    main()
