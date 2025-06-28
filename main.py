import arcade

from player import Player
from aliens import Enemies

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Invasion AAAAAHHHHH!!!!"

PLAYER_MOVEMENT_SPEED = 5
ENEMY_MOVEMENT_SPEED = 1
BOSS_MOVEMENT_SPEED = 2

PLAYER_BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4

BOSS_HP = 5

ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = SCREEN_WIDTH - ENEMY_VERTICAL_MARGIN
LEFT_ENEMY_BORDER = ENEMY_VERTICAL_MARGIN

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        self.enemy_change_x = -ENEMY_MOVEMENT_SPEED
        self.big_boss_change = -BOSS_MOVEMENT_SPEED

    def setup(self):
        self.enemies = Enemies()
        self.player = Player()

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        if self.enemies:
            self.enemies.draw()
        self.enemies.enemy_list.draw()
        self.player.player_bullet_list.draw()


#update each frame
    def on_update(self, delta_time):
        self.player_list.update()
        self.update_enemies()
        self.update_big_boss()
        self.player.player_bullet_list.update()
        for bullet in self.player.player_bullet_list:
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()
        self.process_player_bullets()

    def update_big_boss(self):
        for enemy in self.enemies.bigBoss_list:
            enemy.center_x += self.big_boss_change

        for enemy in self.enemies.bigBoss_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.big_boss_change > 0:
                self.big_boss_change *= -1
                break
            if enemy.left < LEFT_ENEMY_BORDER and self.big_boss_change < 0:
                self.big_boss_change *= -1
                break

    def update_enemies(self):
        # Move enemies left or right
        for enemy in self.enemies.enemy_list:
            enemy.center_x += self.enemy_change_x

        # Check if any enemy hits left or right edge, reverse direction
        for enemy in self.enemies.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                break
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                break

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.SPACE:
            if len(self.player.player_bullet_list) < 3:

                bullet = arcade.Sprite(":resources:/images/space_shooter/laserRed01.png", scale=0.5)
                bullet.change_y = +PLAYER_BULLET_SPEED
                bullet.center_x = self.player_sprite.center_x
                bullet.bottom = self.player_sprite.top

                # Add the bullet to the appropriate lists

                self.player.player_bullet_list.append(bullet)
        elif key == arcade.key.ESCAPE:
            self.window.close()
          
    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def process_player_bullets(self):
        # Move bullets
        self.player.player_bullet_list.update()

        # Loop through each bullet
        for bullet in self.player.player_bullet_list:

            # Check collision with Boss
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies.bigBoss_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for boss in hit_list:
                    if BOSS_HP > 0:
                        BOSS_HP - 1
                    else:
                        boss.remove_from_sprite_lists()
                continue

            # Check collision with enemies
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()

            # Remove bullet if it flies off top of screen
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()


