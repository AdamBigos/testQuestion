from enum import Enum


class Direction(str, Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake(GameObject):
    def __init__(self, x, y, body, direction):
        self.body = body
        self.direction = direction
        super().__init__(x, y)

    def change_direction(self, *, to):
        if to == Direction.UP:
            if self.direction == Direction.DOWN:
                self.y += 10
            else:
                self.y -= 10
                self.direction = Direction.UP

        elif to == Direction.DOWN:
            if self.direction == Direction.UP:
                self.y -= 10
            else:
                self.y += 10
                self.direction = Direction.DOWN

        elif to == Direction.LEFT:
            if self.direction == Direction.RIGHT:
                self.x += 10
            else:
                self.x -= 10
                self.direction = Direction.LEFT

        elif to == Direction.RIGHT:
            if self.direction == Direction.LEFT:
                self.x -= 10
            else:
                self.x += 10
                self.direction = Direction.RIGHT


class Food(GameObject):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y)
