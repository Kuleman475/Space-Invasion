import arcade

class Player():
    def __init__(self):
        #super().__init__(":resources:/images/space_shooter/playerShip1_blue.png", scale=0.5)
        self.player = arcade.Sprite(":resources:/images/space_shooter/playerShip1_blue.png", scale=0.5)
        self.center_x = 680
        self.center_y = 50
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.player_list = arcade.SpriteList()

        self.player_bullet_list = arcade.SpriteList()