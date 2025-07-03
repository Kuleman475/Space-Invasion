import arcade

class Enemies:
    def __init__(self):
        self.bigBossHP = 5
        # Big boss sprite
        self.bigBoss = arcade.Sprite(":resources:/images/alien/alienBlue_front.png", scale=0.5)
        self.bigBoss.center_x = 680
        self.bigBoss.center_y = 650
        self.bigBoss_list = arcade.SpriteList()
        self.bigBoss_list.append(self.bigBoss)

        # Enemies
        self.enemy_list = arcade.SpriteList()

        # Add enemies at specific coordinates
        coordinate_list = [
            [75, 550],
            [150, 550],
            [225, 550],
            [300, 550],
            [375, 550],
            [450, 550],
            [525, 550],
            [600, 550],
            [675, 550],
            [750, 550],
            [825, 550],
            [900, 550],
            [975, 550],
            [1050, 550],
            [1125, 550],
            [1200, 550],
            [1275, 550],
        ]
        for coordinate in coordinate_list:
            crate = arcade.Sprite(":resources:/images/enemies/slimeBlock.png", scale=0.5)
            crate.position = coordinate
            self.enemy_list.append(crate)

        self.enemy_bullet_list = arcade.SpriteList()

    def draw(self):
        # Draw boss and all enemies
        self.bigBoss.draw()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

