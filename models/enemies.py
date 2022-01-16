"""Enemy classes"""

import random

from models.projectiles import Projectile


class Enemy:
    """Enemy super class"""

    def __init__(self, init_row: int, init_col: int, direction: int, max_yx: tuple[int, int]) -> None:
        self.row = init_row
        self.col = init_col
        self.direction = direction
        self.counter = 0
        self.speed = 500
        self.health = 1
        self.max_yx = max_yx
        self.char = '\u237E'

    def update_position(self) -> None:
        """Update enemy position on screen (right: 261, left: 260, up: 259, down: 258)"""
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

    def update_health(self, projectiles: list[Projectile]) -> None:
        """Check if enemy has been hit by projectile and update health"""
        for projectile in projectiles:
            if projectile.row == self.row and projectile.col == self.col:
                self.health -= projectile.damage

    def remove_enemy(self) -> tuple[bool, str]:
        """Check if enemy left screen or has no health"""
        if self.row == 0:
            return True, 'OFF SCREEN'
        if self.row == self.max_yx[0] - 2:
            return True, 'OFF SCREEN'
        if self.col == 0:
            return True, 'OFF SCREEN'
        if self.col == self.max_yx[1] - 2:
            return True, 'OFF SCREEN'
        if self.health <= 0:
            return True, 'KILLED'
        return False, ''


class EnemySpawner:
    """Spawn enemies"""

    def __init__(self, max_enemies: int, min_distance: int, max_yx: tuple[int, int]) -> None:
        self.max_enemies = max_enemies
        self.min_distance = min_distance
        self.counter = 0
        self.spawn_speed = 1000
        self.max_yx = max_yx

    def time_to_spawn(self) -> bool:
        """Check if is time to spawn new enemy"""
        self.counter += 1
        if self.counter % self.spawn_speed == 0:
            return True
        return False

    def spawn_enemy(self, player_row: int, player_col: int) -> Enemy:
        """Spawn an enemy with random direction and at a minimum distance to the player"""
        direction = random.choice([258, 259, 260, 261])
        enemy_row = random.choice(range(5, self.max_yx[0] - 4))
        enemy_col = random.choice(range(5, self.max_yx[1] - 4))
        while player_row - enemy_row < self.min_distance and player_col - enemy_col < self.min_distance:
            enemy_row = random.choice(range(5, self.max_yx[0] - 4))
            enemy_col = random.choice(range(5, self.max_yx[1] - 4))
        return Enemy(enemy_row, enemy_col, direction, self.max_yx)
