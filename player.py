import arcade

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:/images/space_shooter/playerShip1_blue.png", scale=0.5)
        self.center_x = 680
        self.center_y = 50

        self.health = 1


        self.player_bullet_list = arcade.SpriteList()