import arcade
import random

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
        self.player = Player()
        self.player_list.append(self.player.player_list)

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
        self.enemies.enemy_bullet_list.update()
        for bullet in self.player.player_bullet_list:
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()
        self.process_player_bullets()
        self.allow_enemies_to_fire()

        for bullet in self.enemies.enemy_bullet_list:
            if bullet.bottom < 0:
                bullet.remove_from_sprite_lists()

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
                    self.enemies.bigBossHP -= 1
                    if self.enemies.bigBossHP <= 0:
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



    def process_enemy_bullets(self):
        self.enemies.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemies.enemy_bullet_list:

            # Check collision with Boss
            hit_list = arcade.check_for_collision_with_list(bullet, self.player.player_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()



    def allow_enemies_to_fire(self):

        x_spawn = []

        for enemy in self.enemies.enemy_list:
            # Slightly higher firing rate
            
            if len(self.enemies.enemy_list) < 5:
                chance = 4 + len(self.enemies.enemy_list) * 3

            else:
                chance = 4 + len(self.enemies.enemy_list) * 20
            
            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                self.create_enemy_bullet(enemy)
                x_spawn.append(enemy.center_x)


    def create_enemy_bullet(self, enemy):
        bullet = arcade.Sprite(":resources:/images/space_shooter/meteorGrey_small1.png", scale=0.5)
        bullet.angle = 0
        bullet.change_y = -ENEMY_BULLET_SPEED
        bullet.center_x = enemy.center_x
        bullet.top = enemy.bottom
        self.enemies.enemy_bullet_list.append(bullet)

        if len(self.enemies.enemy_list) <= 0:
            bossBullet = arcade.Sprite(":resources:/images/space_shooter/meteorGrey_big3.png", scale=0.5)
            bossBullet.angle = 0
            bossBullet.change_y = -ENEMY_BULLET_SPEED + 2
            bossBullet.center_x = enemy.center_x
            bossBullet.top = enemy.bottom
            self.enemies.enemy_bullet_list.append(bullet)


def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()


