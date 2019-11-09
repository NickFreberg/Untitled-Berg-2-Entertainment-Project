import arcade
import pathlib

from enum import auto, Enum
# GLOBALS
W_WIDTH = 1900
W_HEIGHT = 1000

PLYR_MOVE_SPEED = 5

class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class PlayerSprite(arcade.AnimatedWalkingSprite):
    def __init__(self, scale:float, speed:int, life:int, game_window, strength:int):
        super().__init__()
        self.scale = scale
        self.speed = speed
        self.life = life
        self.game = game_window
        self.strength = strength

    def return_life(self):
        return self.life

    def return_strength(self):
        return self.strength

    def gain_strength(self, increase:int):
        return self.strength + increase

    def move(self, direction:MoveEnum):

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

       # self.tileset_loc = pathlib.Path.cwd() / 'Assets' / 'PathAndObjects.tsx'
        #self.map_location = pathlib.Path.cwd() / 'Assets' / 'humble_begins.tmx'
        #self.map_location = pathlib.Path.cwd() / 'Assets' / 'test.tmx'
        self.maplist = None
        #self.walllist = None

        #player inits
        self.player = None
        self.playerList = None

        #power ups/objects
        self.strengthCoin = None
        self.powerUpList = None

    def setup(self):
        arcade.set_background_color(arcade.color.RED_DEVIL)
        self.animate_player_sprite()
        self.spawn_power_up()

        """ Failed map code - use collection of imgs
       # sample_tiles = arcade.tilemap.read_tmx(str(self.tileset_loc))
        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.maplist = arcade.tilemap.process_layer(sample__map, "ground", 1)

        self.walllist = arcade.tilemap.process_layer(sample__map, "walls", 1)
        """

    def spawn_power_up(self):
        strengthCoinPath = pathlib.Path.cwd() / 'Assets' / 'coin_gold.png'
        self.powerUpList = arcade.SpriteList()
        self.strengthCoin = arcade.Sprite(str(strengthCoinPath), 1, center_x= 400, center_y= 200)
        self.powerUpList.append(self.strengthCoin)

    def animate_player_sprite(self):
        # player setup
        playerPath = pathlib.Path.cwd() / 'Assets' / 'scottpilgrim.png'
        self.playerList = arcade.SpriteList()
        self.player = PlayerSprite(.5, PLYR_MOVE_SPEED, 1, game_window=self, strength=3)
        self.player.center_x = 500
        self.player.center_y = 800
        frame = arcade.load_texture(str(playerPath), 0, 0, height=140, width=108)
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(frame)
        self.player.texture = frame
        frame = arcade.load_texture(str(playerPath), 0, 140, height=140, width=108)
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(frame)
        self.player.walk_right_textures = []
        self.player.walk_left_textures = []
        for image_num in range(8):
            frame = arcade.load_texture(str(playerPath), image_num * 108, 0, height=140, width=108)
            self.player.walk_right_textures.append(frame)
        for image_num in range(8):
            frame = arcade.load_texture(str(playerPath), image_num * 108, 140, height=140, width=108)
            self.player.walk_left_textures.append(frame)
        self.playerList.append(self.player)

    def on_key_press(self, key: int, modifiers: int):
        """ Movement"""
        if key == arcade.key.LEFT:
            self.player.change_x = -PLYR_MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLYR_MOVE_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = PLYR_MOVE_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLYR_MOVE_SPEED

    def on_key_release(self, key: int, modifiers: int):
        """ Movement"""
        if self.player.change_x < 0 and key == arcade.key.LEFT:
            self.player.change_x = 0
        elif self.player.change_x > 0 and key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif self.player.change_y > 0 and key == arcade.key.UP:
            self.player.change_y = 0
        elif self.player.change_y < 0 and key == arcade.key.DOWN:
            self.player.change_y = 0

    def on_draw(self):
        arcade.start_render()
        self.playerList.draw()
        self.powerUpList.draw()

        #self.maplist.draw()
        #self.walllist.draw()

    def on_update(self, delta_time: float):

        self.playerList.update()
        self.playerList.update_animation()

        #collision test power up here
        for self.strengthCoin in self.powerUpList:
            items_touched = arcade.check_for_collision_with_list(self.strengthCoin, self.playerList)
            if len(items_touched) > 0:
                self.strengthCoin.kill()


def main():
    """The Main Method"""
    window = MultiLayeredWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
