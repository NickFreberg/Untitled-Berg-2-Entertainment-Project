import arcade
import pathlib

from enum import auto, Enum
# GLOBALS
W_WIDTH = 1000
W_HEIGHT = 1000

PLYR_MOVE_SPEED = 5

class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class PlayerSprite(arcade.AnimatedWalkingSprite):
    def __init__(self, speed:int, life:int, game_window):
        super().__init__()
        self.speed = speed
        self.life = life
        self.game = game_window

    def return_life(self):
        return self.life

    def move(self, direction:MoveEnum):
        #as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN:
            self.center_y -= self.speed
        elif direction == MoveEnum.LEFT:
            self.center_x -=self.speed
        elif direction == MoveEnum.RIGHT:
            self.center_x += self.speed
        else: #should be MoveEnum.NONE
            pass

class MultiLayeredWindow (arcade.Window):
    def __init__(self):
        super().__init__(W_WIDTH, W_HEIGHT, "Layerssz")

       # self.map_location = pathlib.Path.cwd() / 'Assets' / 'map3.tmx'
        self.maplist = None

        #player inits

        self.player = None
        self.playerlist = None
        self.direction = MoveEnum.NONE


    def setup(self):
        arcade.set_background_color(arcade.color.RED_DEVIL)

        playerPath = pathlib.Path.cwd() / 'Assets' / 'scottpilgrim.png'
        self.playerlist = arcade.SpriteList()
        self.player = PlayerSprite(PLYR_MOVE_SPEED, 1, game_window=self )
        self.player.center_x = 400
        self.player.center_y = 400

        frame = arcade.load_texture(str(playerPath), 0, 0, 102, 120)
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(frame)
        self.player.texture = frame


        self.playerlist.append(self.player)

       # sample__map = arcade.tilemap.read_tmx(str(self.map_location))
       # self.maplist = arcade.tilemap.process_layer(sample__map, "map_layer", 1)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.direction  = MoveEnum.LEFT
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLYR_MOVE_SPEED
    def on_key_release(self, key: int, modifiers: int):

        if self.player.change_x < 0 and key == arcade.key.LEFT:
            self.player.change_x = 0
        elif self.player.change_x > 0 and key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        arcade.start_render()
        self.playerlist.draw()
"""
    def on_update(self, delta_time: float):
        self.playerlist.update()
        self.playerlist.update_animation()
"""



def main():
    """The Main Method"""
    window = MultiLayeredWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
