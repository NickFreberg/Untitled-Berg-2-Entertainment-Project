import arcade
import pathlib

from enum import auto, Enum
# GLOBALS
W_WIDTH = 1900
W_HEIGHT = 1000

PLYR_MOVE_SPEED = 5

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


class EnemySprite(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, speed: int, life: int, game_window, strength: int):
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


class MultiLayeredWindow (arcade.Window):
    def __init__(self):
        super().__init__(W_WIDTH, W_HEIGHT, "Layerssz")
        self.maplist = None


        #player inits
        self.player = None
        self.playerList = None
        self.player_inventory = []
        #power ups/objects
        self.strengthCoin = None
        self.strCoinList = None

        # enemies inits
        self.firstEnemy = None
        self.enemyList = None

    def setup(self):
        arcade.set_background_color(arcade.color.RED_DEVIL)

        self.strCoinList = arcade.SpriteList()

        self.spawn_strength_coin("coin_gold.png", 700, 600)
        self.spawn_strength_coin("coin_gold.png", 800, 600)
        # player movement setup
        playerIdlePath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Idle.png'
        playerRunPath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Run.png'
        self.playerList = arcade.SpriteList()
        self.player = PlayerSprite(1, PLYR_MOVE_SPEED, 2, game_window=self, strength=3)
        self.player.center_x = 500
        self.player.center_y = 800
        self.player.stand_right_textures = []
        self.player.stand_left_textures = []
        frame = arcade.load_texture(str(playerIdlePath), 0, 0, height=137, width=184)
        self.player.texture = frame
        self.player.stand_right_textures.append(frame)
        frame = arcade.load_texture(str(playerIdlePath), 0, 0, height=137, width=184, mirrored=True)
        self.player.stand_left_textures.append(frame)

        self.player.walk_right_textures = []
        self.player.walk_left_textures = []
        for image_num in range(6):
            frame = arcade.load_texture(str(playerRunPath), image_num * 184, 0, height=137, width=184)
            self.player.walk_right_textures.append(frame)
        for image_num in range(6):
            frame = arcade.load_texture(str(playerRunPath), image_num * 184, 0, height=137, width=184, mirrored=True)
            self.player.walk_left_textures.append(frame)
        self.playerList.append(self.player)
        # end player movement

    def spawn_strength_coin(self, img_path, x, y):

        strength_coin_Path = pathlib.Path.cwd() / 'Assets' / img_path

        self.strengthCoin = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
        coin_frames = []
        for col in range(8):
            frame = arcade.load_texture(str(strength_coin_Path), x=col*32, y=0, height=32, width=32)
            coin_frames.append(frame)
        self.strengthCoin.textures = coin_frames
        self.strCoinList.append(self.strengthCoin)

    #def spawn_skull(self):

    def manageInventory(self):
        for power in self.player_inventory:
            print(str(power))
            print("x")

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

        elif key == arcade.key.SPACE:
            print(self.player.strength)


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

        self.strCoinList.draw()


    def on_update(self, delta_time: float):

        self.playerList.update()
        self.playerList.update_animation()

        self.strCoinList.update()
        self.strCoinList.update_animation()

        # collision test power up here
        for self.strengthCoin in self.strCoinList:
            self.strengthCoin.draw()
            items_touched = arcade.check_for_collision_with_list(self.strengthCoin, self.playerList)
            if len(items_touched) > 0:
                self.strengthCoin.kill()
                self.player.strength += 1
                self.player_inventory.append(self.strengthCoin)


def main():
    """The Main Method"""
    window = MultiLayeredWindow()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
