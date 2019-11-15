import arcade
import pathlib

from enum import auto, Enum
# GLOBALS
W_WIDTH = 1200
W_HEIGHT = 800

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

    def patrol(self):
        for x in range(4):
            self.center_x += 2
            self.center_x -= 2





class MultiLayeredWindow (arcade.Window):
    def __init__(self):
        super().__init__(W_WIDTH, W_HEIGHT, "Layerssz")
        # self.tileset_loc = pathlib.Path.cwd() / 'Assets' / 'RPG.tsx'
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'Map1.tmx'
        # self.map_location = pathlib.Path.cwd() / 'Assets' / 'test.tmx'
        self.floorlist = None
        self.wallslist = None
        self.pathlist = None
        self.simple_Physics: arcade.PhysicsEngineSimple = None


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
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)
        self.intro()
        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.floorlist = arcade.tilemap.process_layer(sample__map, "Grass", 1)
        self.wallslist = arcade.tilemap.process_layer(sample__map, "Trees", 1)
        self.pathlist = arcade.tilemap.process_layer(sample__map, "Paths", 1)
        self.strCoinList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.spawn_strength_coin("coin_gold.png", 700, 600)
        self.spawn_strength_coin("coin_gold.png", 800, 600)
        self.spawn_skull()

        # player movement setup
        playerIdlePath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Idle.png'
        playerRunPath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Run.png'
        self.playerList = arcade.SpriteList()
        self.player = PlayerSprite(1, PLYR_MOVE_SPEED, 2, game_window=self, strength=3)
        self.player.center_x = 700
        self.player.center_y = 700
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
        self.simple_Physics = arcade.PhysicsEngineSimple(self.player, self.wallslist)

    def spawn_strength_coin(self, img_path, x, y):

        strength_coin_Path = pathlib.Path.cwd() / 'Assets' / img_path

        self.strengthCoin = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
        coin_frames = []
        for col in range(8):
            frame = arcade.load_texture(str(strength_coin_Path), x=col*32, y=0, height=32, width=32)
            coin_frames.append(frame)
        self.strengthCoin.textures = coin_frames
        self.strCoinList.append(self.strengthCoin)

    def spawn_skull(self):

        self.firstEnemy = EnemySprite(1, PLYR_MOVE_SPEED, 1, game_window=self, strength=1)

        skullPath = pathlib.Path.cwd() / 'Assets' / 'enemies' / 'fire-skull.png'

        self.firstEnemy.center_x = 900
        self.firstEnemy.center_y = 700
        self.firstEnemy.stand_right_textures = []
        self.firstEnemy.stand_left_textures = []
        frame = arcade.load_texture(str(skullPath), 0, 0, height=112, width=17.5)
        self.firstEnemy.texture = frame
        self.firstEnemy.stand_right_textures.append(frame)
        frame = arcade.load_texture(str(skullPath), 0, 0, height=112, width=17.5, mirrored=True)
        self.firstEnemy.stand_left_textures.append(frame)

        self.firstEnemy.walk_right_textures = []
        self.firstEnemy.walk_left_textures = []
        for image_num in range(4):
            frame = arcade.load_texture(str(skullPath), image_num * 17.5, 0, height=112, width=17.5)
            self.firstEnemy.walk_right_textures.append(frame)
        for image_num in range(4):
            frame = arcade.load_texture(str(skullPath), image_num * 17.5, 0, height=112, width=17.5, mirrored=True)
            self.firstEnemy.walk_left_textures.append(frame)
        self.enemyList.append(self.firstEnemy)


    def manageInventory(self):

        for power in self.player_inventory:
            print(str(power))
            print("x")

    def on_key_press(self, key: int, modifiers: int):
        """ Movement"""
        if key == arcade.key.LEFT:
            if self.player.left > 0:
                self.player.change_x = -PLYR_MOVE_SPEED
        elif key == arcade.key.RIGHT:
            if self.player.right < W_WIDTH:
                self.player.change_x = PLYR_MOVE_SPEED
        elif key == arcade.key.UP:
            if self.player.top > 0:
                self.player.change_y = PLYR_MOVE_SPEED
        elif key == arcade.key.DOWN:
            if self.player.bottom < W_HEIGHT:
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
        self.floorlist.draw()
        self.wallslist.draw()
        self.pathlist.draw()
        self.playerList.draw()
        self.strCoinList.draw()
        self.enemyList.draw()

    def on_update(self, delta_time: float):

        self.playerList.update()
        self.playerList.update_animation()
        self.firstEnemy.patrol()
        self.strCoinList.update()
        self.strCoinList.update_animation()
        self.simple_Physics.update()

        # collision test power up here
        for self.strengthCoin in self.strCoinList:
            self.strengthCoin.draw()
            items_touched = arcade.check_for_collision_with_list(self.strengthCoin, self.playerList)
            if len(items_touched) > 0:
                self.strengthCoin.kill()
                self.player.strength += 1
                self.player_inventory.append(self.strengthCoin)

    def intro(self):
        output = f"Player strength: {0}"
        arcade.draw_text(output, 10, 10, arcade.color.WHITE, 13)



def main():
    """The Main Method"""
    window = MultiLayeredWindow()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
