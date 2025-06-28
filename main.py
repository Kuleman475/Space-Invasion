import arcade

from player import Player
from aliens import Enemies

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Invasion AAAAAHHHHH!!!!"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

    def setup(self):
        self.enemies = Enemies()

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        if self.enemies:
            self.enemies.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.center_x -= 10
        elif key == arcade.key.RIGHT:
            self.player_sprite.center_x += 10

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
