import arcade

class Enemies:
    def __init__(self):
        # Big boss sprite
        self.bigBoss = arcade.Sprite(":resources:/images/alien/alienBlue_front.png", scale=0.5)
        self.bigBoss.center_x = 680
        self.bigBoss.center_y = 650

        # Walls / slimes
        self.wall_list = arcade.SpriteList()

        # Add grass tiles
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Add crates at specific coordinates
        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=0.5)
            crate.position = coordinate
            self.wall_list.append(crate)

    def draw(self):
        # Draw boss and all walls/crates
        self.bigBoss.draw()
        self.wall_list.draw()
