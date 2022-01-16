""""Player class"""

from models.projectiles import Projectile
from models.enemies import Enemy


class Player:
    """Player class"""

    def __init__(self, init_row: int, init_col: int, max_yx: tuple[int, int]) -> None:
        self.row = init_row
        self.col = init_col
        self.max_yx = max_yx
        self.chars_dict = {'up': '\u2191', 'down': '\u2193', 'right': '\u2192', 'left': '\u2190'}
        self.char = self.chars_dict['right']

    def update_position(self, direction: int) -> None:
        """Update player position and direction on screen (right: 261, left: 260, up: 259, down: 258)"""
        if direction == 259:
            self.row -= 1
            self.char = self.chars_dict['up']
        elif direction == 258:
            self.row += 1
            self.char = self.chars_dict['down']
        elif direction == 261:
            self.col += 1
            self.char = self.chars_dict['right']
        elif direction == 260:
            self.col -= 1
            self.char = self.chars_dict['left']
        self.row = max(self.row, 0)
        self.row = min(self.row, self.max_yx[0] - 2)
        self.col = max(self.col, 0)
        self.col = min(self.col, self.max_yx[1] - 2)

    def check_health(self, projectiles: list[Projectile], enemies: list[Enemy]) -> bool:
        """Check if player has died"""
        for projectile in projectiles:
            if projectile.row == self.row and projectile.col == self.col:
                return True
        for enemy in enemies:
            if enemy.row == self.row and enemy.col == self.col:
                return True
        return False

    def launch_projectile(self) -> Projectile:
        """Launch projectile from where player is standing in a direction"""
        if self.char == self.chars_dict['up']:
            return Projectile(self.row - 1, self.col, 259, self.max_yx)
        elif self.char == self.chars_dict['down']:
            return Projectile(self.row + 1, self.col, 258, self.max_yx)
        elif self.char == self.chars_dict['right']:
            return Projectile(self.row, self.col + 1, 261, self.max_yx)
        elif self.char == self.chars_dict['left']:
            return Projectile(self.row, self.col - 1, 260, self.max_yx)
