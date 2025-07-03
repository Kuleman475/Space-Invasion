import arcade
import random

from player import Player
from aliens import Enemies

#Screen Information
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Invasion AAAAAHHHHH!!!!"

#Player and NPC Movement speed
PLAYER_MOVEMENT_SPEED = 5
ENEMY_MOVEMENT_SPEED = 1
BOSS_MOVEMENT_SPEED = 2

#Player and NPC bullet speed
PLAYER_BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4

#Borders for Enemies to bounce back and forth
ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = SCREEN_WIDTH - ENEMY_VERTICAL_MARGIN
LEFT_ENEMY_BORDER = ENEMY_VERTICAL_MARGIN

#Sounds for Game
MUSIC = arcade.load_sound("sounds/space.wav")
LASER = arcade.load_sound(":resources:/sounds/laser2.wav")
EXPLODE = arcade.load_sound(":resources:/sounds/explosion1.wav")
ENEMY_FIRE = arcade.load_sound(":resources:/sounds/hit1.wav")
BOSS_FIRE = arcade.load_sound(":resources:/sounds/upgrade1.wav")
ENEMY_DIE = arcade.load_sound(":resources:/sounds/jump1.wav")
BOSS_DIE = arcade.load_sound(":resources:/sounds/gameover4.wav")
BOSS_HIT = arcade.load_sound(":resources:/sounds/hurt3.wav")
BOSS_DEFLECT = arcade.load_sound(":resources:/sounds/error5.wav")

class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.music_playback = arcade.play_sound(MUSIC,  volume=0.25, looping=True)
        
    #Setup movements for enemies and set player
        self.player_list = arcade.SpriteList()
        self.enemy_change_x = -ENEMY_MOVEMENT_SPEED
        self.big_boss_change = -BOSS_MOVEMENT_SPEED

    def setup(self):
    #set enemies and player
        self.enemies = Enemies()
        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
    #put enemies, player, bullets on screen.
        self.player_list.draw()
        if self.enemies:
            self.enemies.draw()
        self.enemies.enemy_list.draw()
        self.player.player_bullet_list.draw()
        arcade.draw_text(
        f"Player: {self.player.health}",
        10, SCREEN_HEIGHT - 30,
        arcade.color.WHITE, 20
        )
    #Boss Hit Points after all enemies gone
        if len(self.enemies.enemy_list) == 0:
            arcade.draw_text(
            f"Boss: {self.enemies.bigBossHP}",
            1250, SCREEN_HEIGHT -30,
            arcade.color.SKY_BLUE, 20
            )
    #Boss has infinite health unless no other enemies on screen
        else:
            arcade.draw_text(
            f"Boss: ---",
            1250, SCREEN_HEIGHT -30,
            arcade.color.SKY_BLUE, 20
            )
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
        self.process_enemy_bullets()

    def update_big_boss(self):
    #Move boss Left or Right    
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
    #Move the player left or right
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
    #Fire Bullets
        elif key == arcade.key.SPACE:
        #Max Bullets 3 and if they go off screen minus bullet
            if len(self.player.player_bullet_list) < 3:
                bullet = arcade.Sprite(":resources:/images/space_shooter/laserRed01.png", scale=0.5)
                bullet.change_y = +PLAYER_BULLET_SPEED
                bullet.center_x = self.player.center_x
                bullet.bottom = self.player.top
                self.player.player_bullet_list.append(bullet)
                self.laser_shot = arcade.play_sound(LASER)
        
        elif key == arcade.key.ESCAPE:
            self.window.close()
          
    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def process_player_bullets(self):
        
        self.player.player_bullet_list.update()

    # Loop through each bullet
        for bullet in self.player.player_bullet_list:

        # Check collision with Boss
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies.bigBoss_list)
            if hit_list:
                bullet.remove_from_sprite_lists()

                if len(self.enemies.enemy_list) ==0:
                    for boss in hit_list:
                        self.enemies.bigBossHP -= 1
                        self.boss_hit = arcade.play_sound(BOSS_HIT)
                        if self.enemies.bigBossHP <= 0:
                            boss.remove_from_sprite_lists()
                            self.boss_die = arcade.play_sound(BOSS_DIE)
                    continue
                else:
                    self.boss_deflect = arcade.play_sound(BOSS_DEFLECT)

        # Check collision with enemies
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.enemy_die = arcade.play_sound(ENEMY_DIE)

        # Remove bullet if it flies off top of screen
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()
    #Check to see if any enemies left on screen
        if len(self.enemies.enemy_list) == 0 and len(self.enemies.bigBoss_list) == 0:
    #If no Enemies you win     
            print("You Win!")
            game_win = GameWin()
            self.window.show_view(game_win)

    def process_enemy_bullets(self):
        self.enemies.enemy_bullet_list.update()

        for bullet in self.enemies.enemy_bullet_list:
            if arcade.check_for_collision(bullet, self.player):
                bullet.remove_from_sprite_lists()
                self.player.health -= 1
                print(f"Player hit! Health left: {self.player.health}")
                if self.player.health <= 0:
                    self.dead = arcade.play_sound(EXPLODE)
                    print("Game Over!")
                    game_over = GameOver()
                    self.window.show_view(game_over)

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
                self.enemy_fire = arcade.play_sound(ENEMY_FIRE)
        
    
        if len(self.enemies.enemy_list) == 0:
            chance = 30
            for boss in self.enemies.bigBoss_list:
                if random.randrange(chance) == 0 and boss.center_x not in x_spawn:
                    self.create_enemy_bullet(boss)
                    x_spawn.append(boss.center_x)
                    self.boss_fire = arcade.play_sound(BOSS_FIRE)

    def create_enemy_bullet(self, enemy):
        bullet = arcade.Sprite(":resources:/images/space_shooter/meteorGrey_small1.png", scale=0.5)
        bullet.angle = 0
        bullet.change_y = -ENEMY_BULLET_SPEED
        bullet.center_x = enemy.center_x
        bullet.top = enemy.bottom
        self.enemies.enemy_bullet_list.append(bullet)

        if len(self.enemies.enemy_list) == 0:
            bossBullet = arcade.Sprite(":resources:/images/space_shooter/meteorGrey_big3.png", scale=1)
            bossBullet.angle = 0
            bossBullet.change_y = -ENEMY_BULLET_SPEED + 2
            bossBullet.center_x = enemy.center_x
            bossBullet.top = enemy.bottom
            self.enemies.enemy_bullet_list.append(bossBullet)

#Game Over Screen
class GameOver(arcade.View):

    def __init__(self):
       super().__init__()

    def on_show_view(self):

        self.window.background_color = arcade.color.BLACK

    def on_draw(self):

        self.clear()
        arcade.draw_text(
            "Game Over",
            start_x=SCREEN_WIDTH/2, 
            start_y=360, 
            color=arcade.color.WHITE, 
            font_size=60, 
            anchor_x="center")

        arcade.draw_text(
            "Click to restart",
            start_x=SCREEN_WIDTH / 2,
            start_y=300,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center")
        
#Press mouse to play again
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

#Press Space to play again
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)

#You Win Screen
class GameWin(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):

        self.clear()
#Say you win on screen        
        arcade.draw_text(
            "You WIN!!",
            start_x=SCREEN_WIDTH/2, 
            start_y=360, 
            color=arcade.color.BLUE, 
            font_size=60, 
            anchor_x="center")
        
#Say Click to play again on screen
        arcade.draw_text(
            "Click to Play Again",
            start_x=SCREEN_WIDTH / 2,
            start_y=300,
            color=arcade.color.BLUE,
            font_size=24,
            anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()