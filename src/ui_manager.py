import pygame

class UIManager:
    """
    Manages the user interface elements, including text rendering for scores,
    messages (game over, pause), and dialogs. It uses themed settings for
    fonts and colors.
    """
    def __init__(self, screen_width, screen_height, theme):
        """
        Initializes the UIManager with screen dimensions and a theme.
        Args:
            screen_width (int): The width of the game screen.
            screen_height (int): The height of the game screen.
            theme (dict): A dictionary containing theme settings like colors and font details.
        """
        pygame.font.init() # Ensure font module is initialized
        self.theme = theme
        self.text_color = theme["text_color"]
        self.score_font = pygame.font.Font(theme.get("font_name"), theme.get("font_size_score", 36))
        self.message_font = pygame.font.Font(theme.get("font_name"), theme.get("font_size_message", 48))
        self.small_message_font = pygame.font.Font(theme.get("font_name"), theme.get("font_size_small_message", 36))

        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw_score(self, screen, score):
        """Renders the current score on the screen."""
        score_surface = self.score_font.render(f"Score: {score}", True, self.text_color)
        screen.blit(score_surface, (10, 10))

    def draw_game_over_message(self, screen, final_score, high_score):
        """
        Renders the 'Game Over' message, final score, high score, and restart instructions.
        Args:
            screen: The Pygame screen surface to draw on.
            final_score (int): The player's score for the ended game.
            high_score (int): The current high score.
        """
        # Main "Game Over" message
        game_over_surface = self.message_font.render("Game Over", True, self.text_color)
        game_over_rect = game_over_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 70))
        screen.blit(game_over_surface, game_over_rect)

        # Final score
        final_score_surface = self.small_message_font.render(f"Final Score: {final_score}", True, self.text_color)
        final_score_rect = final_score_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 20))
        screen.blit(final_score_surface, final_score_rect)

        # High Score
        high_score_surface = self.small_message_font.render(f"High Score: {high_score}", True, self.text_color)
        high_score_rect = high_score_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 20))
        screen.blit(high_score_surface, high_score_rect)

        # Restart instructions
        restart_surface = self.small_message_font.render("Press 'R' to Restart", True, self.text_color)
        restart_rect = restart_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 70))
        screen.blit(restart_surface, restart_rect)

    def draw_pause_message(self, screen):
        """Renders the 'Paused' message on the screen."""
        pause_surface = self.message_font.render("Paused", True, self.text_color)
        pause_rect = pause_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        screen.blit(pause_surface, pause_rect)

    def draw_confirmation_dialog(self, screen, message):
        """
        Renders a confirmation dialog with the given message.
        Args:
            screen: The Pygame screen surface to draw on.
            message (str): The message to display in the dialog.
        """
        dialog_surface = self.small_message_font.render(message, True, self.text_color)
        dialog_rect = dialog_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

        # Optional: Draw a background box for the dialog
        padding = 20
        bg_rect = pygame.Rect(
            dialog_rect.left - padding, dialog_rect.top - padding,
            dialog_rect.width + padding * 2, dialog_rect.height + padding * 2
        )
        bg_rect.center = dialog_rect.center # Ensure it's centered on text after padding

        pygame.draw.rect(screen, (50, 50, 50), bg_rect) # Dark grey background
        pygame.draw.rect(screen, self.text_color, bg_rect, 2) # Border for the box
        screen.blit(dialog_surface, dialog_rect)
