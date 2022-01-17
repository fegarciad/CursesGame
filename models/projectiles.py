"""Projectile classes"""


class Projectile:
    """Projectile super class"""

    def __init__(self, init_row: int, init_col: int, direction: int, max_yx: tuple[int, int]) -> None:
        self.row = init_row
        self.col = init_col
        self.direction = direction
        self.damage = 1
        self.counter = 0
        self.speed = 50
        self.max_yx = max_yx
        self.char = '\u2600'

    def update_position(self) -> None:
        """Update projectile position on screen (right: 261, left: 260, up: 259, down: 258)"""
        self.counter += 1
        if self.counter % self.speed == 0:
            if self.direction == 259:
                self.row -= 1
            elif self.direction == 258:
                self.row += 1
            elif self.direction == 261:
                self.col += 1
            elif self.direction == 260:
                self.col -= 1
        self.row = max(self.row, 0)
        self.row = min(self.row, self.max_yx[0] - 2)
        self.col = max(self.col, 0)
        self.col = min(self.col, self.max_yx[1] - 2)

    def remove_projectile(self) -> bool:
        """Check if projectile left screen"""
        if self.row == 0:
            return True
        if self.row == self.max_yx[0] - 2:
            return True
        if self.col == 0:
            return True
        if self.col == self.max_yx[1] - 2:
            return True
        return False
