class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_score_to_string(self, score):
        print(f"Score: {score}")

    def draw_game_over_message_to_string(self, score, high_score):
        print("Game Over")
        print(f"Score: {score}")
        print(f"High Score: {high_score}")
        print("Press 'r' to restart")

    def draw_pause_message_to_string(self):
        print("Paused")

    def draw_confirmation_dialog_to_string(self, message):
        print(message)
