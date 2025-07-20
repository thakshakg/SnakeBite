import random

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.spawn([])

    def spawn(self, snake_body):
        print("Spawning food...")
        while True:
            self.position = (random.randint(0, self.width - 1),
                             random.randint(0, self.height - 1))
            print(f"Trying to spawn at {self.position}")
            if self.position not in snake_body:
                print(f"Food spawned at {self.position}")
                break

    def is_eaten(self, snake_head, snake_body):
        if snake_head == self.position:
            self.spawn(snake_body)
            return True
        return False

    def draw_to_string(self, board):
        if 0 <= self.position[1] < len(board) and 0 <= self.position[0] < len(board[0]):
            board[self.position[1]][self.position[0]] = "*"
