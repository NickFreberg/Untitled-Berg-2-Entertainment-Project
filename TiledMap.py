import arcade
import pathlib

from enum import auto, Enum
# GLOBALS
W_WIDTH = 1900
W_HEIGHT = 1000

PLYR_MOVE_SPEED = 5

class PlayerSprite(arcade.AnimatedWalkingSprite):
    def __init__(self, scale:float, state:str, life:int, game_window, strength:int):
        super().__init__()
        self.scale = scale
        self.state = state
        self.life = life
        self.game = game_window
        self.strength = strength

class EnemySkull(arcade.AnimatedTimeSprite):

    def _init_(self):
        super().__init__()
        self.speed = 2
        self.life = 5
        self.attack = 2

    def update(self):
        self.center_x += 1



class MultiLayeredWindow(arcade.Window):
    def __init__(self):
        super().__init__(W_WIDTH, W_HEIGHT, "Layerssz")

        #some paths
        # self.tileset_loc = pathlib.Path.cwd() / 'Assets' / 'RPG.tsx'
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'Map1.tmx'
        # self.map_location = pathlib.Path.cwd() / 'Assets' / 'test.tmx'

        self.skull_animation = pathlib.Path.cwd() / 'Assets' / "enemies" / "fire-skull-no-fire.png"


        self.floorlist = None
        self.wallslist = None
        self.simple_Physics: arcade.PhysicsEngineSimple = None


        #player inits
        self.player = None
        self.playerList = None
        self.player_direction = ""
        self.player_inventory = []
        #power ups/objects
        self.strengthCoin = None
        self.strCoinList = None

        # enemies inits
        self.firstEnemy = None
        self.enemyList = None

    def setup(self):
        self.frame_count = 0.0
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.floorlist = arcade.tilemap.process_layer(sample__map, "Grass", 1)
        self.wallslist = arcade.tilemap.process_layer(sample__map, "Trees", 1)
        self.strCoinList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.spawn_strength_coin("coin_gold.png", 700, 600)
        self.spawn_strength_coin("coin_gold.png", 800, 600)

        #enemy setup - reg skull
        self.firstEnemy = arcade.Sprite(str(self.skull_animation),scale=1, image_width=54, image_height=70, center_x= 900, center_y=600)
        self.enemyList.append(self.firstEnemy)


#        self.simple_Physics = arcade.PhysicsEngineSimple(self.player, self.wallslist)

        # player movement setup
        player_idle_ath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Idle.png'
        player_run_path = pathlib.Path.cwd() / 'Assets' / 'player' / 'Run.png'
        self.playerList = arcade.SpriteList()
        self.player = PlayerSprite(1, "idle", 10, game_window=self, strength=3)
        self.player.position = 500, 600
        self.player.stand_right_textures = []
        self.player.stand_left_textures = []
        #stand right/left
        frame = arcade.load_texture(str(player_idle_ath), 0, 0, height=137, width=184)
        self.player.texture = frame
        self.player.stand_right_textures.append(frame)
        frame = arcade.load_texture(str(player_idle_ath), 0, 0, height=137, width=184, mirrored=True)
        self.player.stand_left_textures.append(frame)
        #walk right/left
        self.player.walk_right_textures = []
        self.player.walk_left_textures = []
        for image_num in range(8):
            frame = arcade.load_texture(str(player_run_path), image_num * 184, 0, height=137, width=184)
            self.player.walk_right_textures.append(frame)
        for image_num in range(8):
            frame = arcade.load_texture(str(player_run_path), image_num * 184, 0, height=137, width=184, mirrored=True)
            self.player.walk_left_textures.append(frame)

        # end player movement
        # player attack textures start

        player_attack_path = pathlib.Path.cwd() / 'Assets' / 'player' / 'Attack1.png'
        for col in range(4):
            plyr_atk_frame = arcade.load_texture(player_attack_path, x=col * 184, width=184, height=137)
            self.player.append_texture(plyr_atk_frame)

        for col in range(4):
            plyr_atk_frame = arcade.load_texture(player_attack_path, x=col * 184, width=184, height=137, mirrored=True)
            self.player.append_texture(plyr_atk_frame)

        self.playerList.append(self.player)

    def intro(self):
        """displays life points"""
        output = f"Player Life points: " + str(self.player.life) + f"\nPlayer Strength points:" + str(
            self.player.strength)
        arcade.draw_text(output, 50, 900, arcade.color.BLACK_BEAN, 13)

    def spawn_strength_coin(self, img_path, x, y):

        strength_coin_Path = pathlib.Path.cwd() / 'Assets' / img_path

        self.strengthCoin = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
        coin_frames = []
        for col in range(8):
            frame = arcade.load_texture(str(strength_coin_Path), x=col*32, y=0, height=32, width=32)
            coin_frames.append(frame)
        self.strengthCoin.textures = coin_frames
        self.strCoinList.append(self.strengthCoin)

    def manageInventory(self):

        for power in self.player_inventory:
            print(str(power))
            print("x")

    def on_key_press(self, key: int, modifiers: int):
        """ Movement"""
        if key == arcade.key.LEFT:
            self.player_direction = "left"
            self.player.change_x = -PLYR_MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_direction = "right"
            self.player.change_x = PLYR_MOVE_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = PLYR_MOVE_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLYR_MOVE_SPEED

        if key == arcade.key.SPACE:
          if self.player_direction == "right":
                self.player.texture = self.player.textures[2]
          elif self.player_direction == "left":
                self.player.texture = self.player.textures[6]

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
        self.intro()
        self.floorlist.draw()
        self.wallslist.draw()
        self.playerList.draw()
        self.strCoinList.draw()
        self.enemyList.draw()

        # self.firstEnemy.draw()



    def on_update(self, delta_time: float):

        self.frame_count += .02
        print(self.frame_count)

        self.playerList.update()
        self.playerList.update_animation()

        self.strCoinList.update()
        self.strCoinList.update_animation()

        # ENEMY ATK
        #skull collision deals dmg
        #-1 life point (lp)
        # CHANGE THE sprite hit box value
        # ADD DELAY
        for self.firstEnemy in self.enemyList:
            skull_atk = arcade.check_for_collision_with_list(self.player, self.enemyList)
            if len(skull_atk) > 0 and self.player.state != "damaged":
            #rewrite for delay ^ len... && self.player.state != damaged
                self.player.life -= 1
                # get projctile




        # PICK UP COIN
        # ADDS  TO STR VAL
        for self.strengthCoin in self.strCoinList:
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
