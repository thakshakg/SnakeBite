import curses
import json
import os
import time
from .gameboard import GameBoard

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")

def create_default_config():
    return {
        "screen_width": 80,
        "screen_height": 24,
        "fps": 10,
        "high_score": 0,
        "initial_snake_length": 3,
        "points_per_food": 10,
        "snake_speed_increment_factor": 0.0,
    }

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
            default_config_template = create_default_config()
            for key, default_value in default_config_template.items():
                if key not in config_data:
                    config_data[key] = default_value
            return config_data
    except (FileNotFoundError, json.JSONDecodeError):
        default_config = create_default_config()
        save_config(default_config)
        return default_config

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2)
    except IOError:
        pass

def main():
    # stdscr = curses.initscr()
    # curses.cbreak()
    # curses.noecho()
    # stdscr.keypad(True)

    try:
        # curses.curs_set(0)
        # stdscr.nodelay(1)
        # stdscr.timeout(100)

        config = load_config()
        screen_width = config.get("screen_width", 80)
        screen_height = config.get("screen_height", 24)
        base_fps = config.get("fps", 10)
        high_score = config.get("high_score", 0)
        initial_snake_length = config.get("initial_snake_length", 3)
        points_per_food = config.get("points_per_food", 10)

        game_board = GameBoard(
            screen_width, screen_height,
            high_score=high_score,
            initial_snake_length=initial_snake_length,
            points_per_food=points_per_food
        )

        running = True
        while running:
            # key = stdscr.getch()
            #
            # if game_board.confirm_quit:
            #     if key == ord('y'):
            #         running = False
            #     elif key == ord('n'):
            #         game_board.confirm_quit = False
            # elif key == 27: # Escape key
            #     if game_board.paused:
            #         game_board.paused = False
            #     elif not game_board.game_over:
            #         game_board.paused = True
            # elif key == ord(' '):
            #     if not game_board.game_over:
            #         game_board.paused = not game_board.paused
            # elif key == ord('r'):
            #     if game_board.game_over:
            #         game_board.reset_game()
            # elif not game_board.paused and not game_board.game_over:
            #     if key == curses.KEY_UP:
            #         game_board.snake.change_direction_up()
            #     elif key == curses.KEY_DOWN:
            #         game_board.snake.change_direction_down()
            #     elif key == curses.KEY_LEFT:
            #         game_board.snake.change_direction_left()
            #     elif key == curses.KEY_RIGHT:
            #         game_board.snake.change_direction_right()
            #     elif key == ord('q'):
            #         game_board.confirm_quit = True

            game_board.update()
            os.system("clear")
            game_board.draw_to_string()
            time.sleep(1 / base_fps)

        config["high_score"] = game_board.high_score
        save_config(config)
    finally:
        pass
        # curses.nocbreak()
        # stdscr.keypad(False)
        # curses.echo()
        # curses.endwin()

if __name__ == '__main__':
    main()
