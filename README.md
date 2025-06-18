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

## Running with Docker

This application can be built and run using Docker and Docker Compose, which helps manage the Pygame environment and its dependencies.

### Prerequisites

*   **Docker:** Ensure Docker is installed and running on your system. [Get Docker](https://docs.docker.com/get-docker/)
*   **Docker Compose:** Ensure Docker Compose is installed (usually included with Docker Desktop). [Install Docker Compose](https://docs.docker.com/compose/install/)
*   **X Server (Linux/macOS):** Your host machine must have an X server running.
    *   **Linux:** This is typically standard.
    *   **macOS:** You'll need to install and run [XQuartz](https://www.xquartz.org/).
    *   **Windows:** You can use WSLg (if using WSL 2) or install a third-party X server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/).
*   **X11 Forwarding Setup (Important):**
    *   For the GUI to appear on your host screen, X11 forwarding needs to be configured.
    *   **Linux:** You may need to allow local connections to your X server. Run the following command in your host's terminal:
        ```bash
        xhost +local:docker
        ```
        To restrict access again after you're done: `xhost -local:docker`
    *   **macOS (with XQuartz):** Ensure XQuartz is running. In XQuartz preferences, go to the "Security" tab and make sure "Allow connections from network clients" is checked. You might also need to run `xhost +localhost` or `xhost +$(ipconfig getifaddr en0)` (or your active network interface).
    *   **Windows (with VcXsrv/Xming):** When launching your X server, ensure that you disable access control (e.g., by checking "Disable access control" in VcXsrv's setup or by adding `-ac` to the command line). Ensure your `DISPLAY` environment variable is correctly set (often `localhost:0.0` or your machine's IP).

### Build and Run

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the project root directory** (where `docker-compose.yml` is located).
3.  **Build the Docker image and run the container:**
    ```bash
    docker-compose up --build
    ```
    *   The `--build` flag ensures the image is built (or rebuilt if changes are detected).
    *   The game window should appear on your host display.

4.  **To stop the application:**
    *   Press `Ctrl+C` in the terminal where `docker-compose up` is running.
    *   To remove the container afterwards: `docker-compose down`

### Development with Docker

If you are developing the game and want to see changes without rebuilding the image every time, you can uncomment the volume mount lines in `docker-compose.yml`:

```yaml
# services:
#   snake_game:
#     ...
#     volumes:
#       - /tmp/.X11-unix:/tmp/.X11-unix:rw
#       # Uncomment these for live code reloading:
#       - ./src:/app/src
#       - ./assets:/app/assets
#       - ./config.json:/app/config.json
#     ...
```
With these lines uncommented, changes to your local `src`, `assets`, or `config.json` files will be reflected inside the running container. You might need to restart the game within the container (if it doesn't auto-reload) or restart the container (`docker-compose restart snake_game`) for some changes to take effect.
