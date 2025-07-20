import random

class Snake:
    def __init__(self, width, height, initial_length=3):
        self.width = width
        self.height = height
        self.segment_size = 1
        self.initial_length = initial_length
        self.reset()

    def reset(self):
        self.body = [(self.width // 2, self.height // 2)]
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        for _ in range(1, self.initial_length):
            self.grow()

    def move(self):
        head = self.body[0]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'LEFT':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'RIGHT':
            new_head = (head[0] + 1, head[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def check_collision(self):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= self.width or
                head[1] < 0 or head[1] >= self.height):
            return True
        if head in self.body[1:]:
            return True
        return False

    def change_direction_up(self):
        if self.direction != 'DOWN':
            self.direction = 'UP'

    def change_direction_down(self):
        if self.direction != 'UP':
            self.direction = 'DOWN'

    def change_direction_left(self):
        if self.direction != 'RIGHT':
            self.direction = 'LEFT'

    def change_direction_right(self):
        if self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def draw_to_string(self, board):
        for i, segment in enumerate(self.body):
            char = "O" if i == 0 else "#"
            if 0 <= segment[1] < len(board) and 0 <= segment[0] < len(board[0]):
                board[segment[1]][segment[0]] = char
