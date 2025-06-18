# Python Snake Game

A classic implementation of the Snake game using Python and the Pygame library. This project aims to provide a fully functional and extendable version of the beloved arcade game.

## Features Implemented

*   **Core Gameplay:**
    *   Continuous snake movement based on the last input direction.
    *   Random food spawning on the grid.
    *   Snake grows longer after eating food.
    *   Game ends on collision with self or screen boundaries.
*   **Graphical User Interface (GUI):**
    *   Built with Pygame for window creation, rendering, and event handling.
    *   Grid-based layout for snake and food.
    *   Score display (top-left corner).
    *   High score display on the game over screen.
    *   Adjustable frame refresh rate (via `config.json`).
*   **Controls:**
    *   **Arrow Keys (Up, Down, Left, Right):** Control snake direction.
    *   **Spacebar:** Pause / Resume game.
    *   **'R' Key:** Restart game after game over.
    *   **ESC Key:** Pause game / Open quit confirmation dialog.
    *   **'Y' Key:** Confirm quit.
    *   **'N' Key:** Cancel quit.
*   **Configuration & Persistence:**
    *   Game settings (screen dimensions, FPS, colors, fonts, sound files) are managed through `config.json`.
    *   High scores are saved and loaded from `config.json`.
*   **Visuals & Audio:**
    *   Customizable color themes for background, snake, food, and text.
    - Customizable fonts for UI text.
    *   Sound effects for eating food and game over events.
*   **Code Structure:**
    *   Modular design with classes for `Snake`, `Food`, `GameBoard`, and `UIManager`.
    *   Separation of game logic and display layers.
    *   Designed for extendibility (e.g., adding power-ups, new game modes).

## Technologies Used

*   **Python 3**
*   **Pygame:** (version will be based on environment, typically latest stable)

## How to Run the Game

1.  **Prerequisites:**
    *   Ensure Python 3 is installed on your system.
    *   You will need the Pygame library.

2.  **Installation:**
    *   Clone the repository (if applicable) or download the source files.
    *   Install Pygame:
        ```bash
        pip install pygame
        ```

3.  **Running the Game:**
    *   Navigate to the project's root directory (where `main.py` is located).
    *   Execute the following command:
        ```bash
        python main.py
        ```

## Game Controls Summary

*   **Up Arrow:** Move Up
*   **Down Arrow:** Move Down
*   **Left Arrow:** Move Left
*   **Right Arrow:** Move Right
*   **Spacebar:** Pause / Resume
*   **R:** Restart Game (when game is over)
*   **ESC:** Pause Game / Open Quit Confirmation (if paused, resumes; if active, pauses; if confirming quit, cancels)
*   **Y:** Yes (to confirm quit)
*   **N:** No (to cancel quit)

## Configuration

The game's behavior and appearance can be customized through the `config.json` file located in the root directory. This includes:

*   Screen width and height
*   Frames Per Second (FPS)
*   High score persistence
*   Color themes for various game elements (background, snake, food, text)
*   Font settings for UI text
*   Paths to sound effect files

If `config.json` is missing or corrupted, a default configuration will be generated on the first run.

## Future Enhancements

This project is designed with extendibility in mind. Potential future enhancements include:

*   **Advanced Game Modes:** Time attack, survival with increasing difficulty, etc.
*   **Power-ups:** Speed boosts, shields, score multipliers, etc.
*   **Obstacles:** Static or moving obstacles on the game board.
*   **Improved Graphics:** Sprite-based graphics, animations.
*   **More Sound Effects & Music:** Background music, more detailed sound events.
*   **AI Opponent/Helper:** An AI-controlled snake or helper.
*   **Level Editor:** Allow users to design their own game boards.

## Contribution Guidelines

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3.  **Make your changes.** Ensure your code adheres to the existing style and is well-commented.
4.  **Test your changes thoroughly.** (Unit tests are planned for future iterations).
5.  **Commit your changes** with a clear and descriptive commit message:
    ```bash
    git commit -m "feat: Implement amazing new feature"
    ```
6.  **Push your changes** to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
7.  **Open a Pull Request** to the main repository, detailing the changes you've made.

Please ensure your contributions are well-tested and align with the project's goals.

---

Enjoy the game!
