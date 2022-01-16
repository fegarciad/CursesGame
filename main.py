"""Main game executable"""

import curses

from models.player import Player
from models.projectiles import Projectile
from models.enemies import EnemySpawner, Enemy

START_ROW, START_COLUMN = 5, 5
MAX_PROJECTILES = 10
MAX_ENEMIES = 10
ENEMY_SPAWN_DISTANCE = 5


def main(stdscr) -> None:
    """Main function"""
    curses.curs_set(0) # Hide cursor
    stdscr.nodelay(True)

    player_score = 0
    player = Player(START_ROW, START_COLUMN, stdscr.getmaxyx())
    enemy_spawner = EnemySpawner(MAX_ENEMIES, ENEMY_SPAWN_DISTANCE, stdscr.getmaxyx())
    projectiles_on_screen: list[Projectile] = []
    enemies_on_screen: list[Enemy] = []

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key in [258, 259, 260, 261]:
            player.update_position(key)
        elif key == 32:
            if len(projectiles_on_screen) < MAX_PROJECTILES:
                projectiles_on_screen.append(player.launch_projectile())
        elif key in [27, 113]:  # Escape or 'q' key to exit
            break
        
        if player.check_health(projectiles_on_screen, enemies_on_screen):
            break
        stdscr.addstr(player.row, player.col, f'{player.char}')
        stdscr.addstr(1, 1, f'Score: {player_score}')

        for i, projectile in enumerate(projectiles_on_screen):
            projectile.update_position()
            stdscr.addstr(projectile.row, projectile.col, f'{projectile.char}')
            if projectile.remove_projectile():
                projectiles_on_screen.pop(i)

        if enemy_spawner.time_to_spawn() and len(enemies_on_screen) < MAX_ENEMIES:
            enemies_on_screen.append(enemy_spawner.spawn_enemy(player.row, player.col))

        for i, enemy in enumerate(enemies_on_screen):
            enemy.update_position()
            enemy.update_health(projectiles_on_screen)
            stdscr.addstr(enemy.row, enemy.col, f'{enemy.char}')
            remove = enemy.remove_enemy()
            if remove[0]:
                enemies_on_screen.pop(i)
                if remove[1] == 'KILLED':
                    player_score += 1

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
