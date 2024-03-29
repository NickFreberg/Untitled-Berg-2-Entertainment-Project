import arcade
import pathlib

# 2D RPG BY
# NICK FREBERG AND RAINA MALMBERG
# move with arrows keys
# attack with SPACEBAR


# UNFINISHED:
# ENEMY AI
# which was tested in FloodFill.py

from enum import auto, Enum
# GLOBALS
W_WIDTH = 608
W_HEIGHT = 608

PLYR_MOVE_SPEED = 5

class Node:
    def init(self):
        self.up: Node = None
        self.down: Node = None
        self.left: Node = None
        self.right: Node = None

    def flood_fill(self, location: list, map, graph):
        #pseudo code
        # if location 1 and the other locations are not empty, return
        if location[1] > 0 and graph[location[1]-1][location[2]] != None:
            return
        # if location 1
        if location[1] > 0 and graph[location[1]-1][location[2]] == None:
            myNode = Node()
            graph[location[1]-1][location[2]] = myNode


class PlayerSprite(arcade.AnimatedWalkingSprite):

    def __init__(self, scale:float, state:str, life:int, game_window, strength:int):
        super().__init__()
        self.scale = scale
        self.state = state
        self.life = life
        self.game = game_window
        self.strength = strength

        # player attack textures start

        player_attack_path = pathlib.Path.cwd() / 'Assets' / 'player' / 'Attack1.png'
        for col in range(4):
            plyr_atk_frame = arcade.load_texture(player_attack_path, x=col * 184, width=184, height=137)
            self.append_texture(plyr_atk_frame)

        for col in range(4):
            plyr_atk_frame = arcade.load_texture(player_attack_path, x=col * 184, width=184, height=137, mirrored=True)
            self.append_texture(plyr_atk_frame)




class MultiLayeredWindow(arcade.Window):
    def __init__(self):
        super().__init__(W_WIDTH, W_HEIGHT, "Berg**2 Game")

        self.current_map = 0
        self.kill_score = 0

        #some paths
        # self.tileset_loc = pathlib.Path.cwd() / 'Assets' / 'RPG.tsx'
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'Home.tmx'
        self.outdoors_map = pathlib.Path.cwd() / 'Assets' / 'Outdoors.tmx'
        # self.tavern_map = pathlib.Path.cwd() / 'Assets' / 'Tavern.tmx'
        # self.map_location = pathlib.Path.cwd() / 'Assets' / 'test.tmx'

        self.my_flood_map = pathlib.Path.cwd() / 'Assets' / '4Rooms' / '4ROOMS.tmx'

        self.player_idle_ath = pathlib.Path.cwd() / 'Assets' / 'player' / 'Idle.png'
        self.player_run_path = pathlib.Path.cwd() / 'Assets' / 'player' / 'Run.png'

        self.skull_animation = pathlib.Path.cwd() / 'Assets' / "enemies" / "fire-skull-no-fire.png"

        #maplists for home for Home
        self.floorlist = None
        self.wallslist = None
        self.doorlist = None
        self.bedlist = None
        self.other1 = None
        self.other2 = None
        self.simple_Physics: arcade.PhysicsEngineSimple = None

        #spritelists for 4Rooms
        self.flood_grass_list = None
        self.flood_walls_list = None

        #player inits
        self.player = None
        self.playerList = None
        self.player_direction = ""
        self.player_inventory = []
        #power ups/objects
        self.strengthCoin = None
        self.strCoinList = None
        self.coin_sound = None
        self.player_sword_sound = None
        self.skull_death = None

        # enemies inits
        self.firstEnemy = None
        self.secondEnemy = None
        self.thirdEnemy = None
        self.fourthEnemy = None
        self.enemyList = None

    def setup(self):
        self.frame_count = 0

        arcade.set_background_color(arcade.color.BLACK)

        flood_map = arcade.tilemap.read_tmx(str(self.my_flood_map))
        self.flood_walls_list = arcade.tilemap.process_layer(flood_map, "WALLS", 1)
        self.flood_grass_list = arcade.tilemap.process_layer(flood_map, "GRASS", 1)

        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        outdoor_map = arcade.tilemap.read_tmx(str(self.outdoors_map))

        # tavern_map = arcade.tilemap.read_tmx(str(self.tavern_map))
        # self.floorlist = arcade.tilemap.process_layer(sample__map, "floor", 1)
        # self.wallslist = arcade.tilemap.process_layer(sample__map, "Walls/Windows", 1)
        # self.doorlist = arcade.tilemap.process_layer(sample__map, "Doors", 1)
        # self.bedlist = arcade.tilemap.process_layer(sample__map, "bed", 1)
        # self.other1 = arcade.tilemap.process_layer(sample__map, "Obstacles/Furniture", 1)
        # self.other2 = arcade.tilemap.process_layer(sample__map, "Tile Layer 6", 1)

        self.floorlist = arcade.tilemap.process_layer(outdoor_map, "Grass", 1)
        self.wallslist = arcade.tilemap.process_layer(outdoor_map, "Wall", 1)
        self.doorlist = arcade.tilemap.process_layer(outdoor_map, "Doors", 1)
        self.bedlist = arcade.tilemap.process_layer(outdoor_map, "Extra Wall", 1)
        self.other1 = None
        self.other2 = None
        self.strCoinList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.spawn_strength_coin("coin_gold.png", 120, 450)
        self.spawn_strength_coin("coin_gold.png", 450, 210)

        # Sounds
        self.player_sword_sound = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'Sword.wav')
        self.skull_death = arcade.load_sound(pathlib.Path.cwd() / 'Assets'/ 'Sounds' / 'EnemyDeath.wav')
        self.coin_sound = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'Coin.wav')

        # player movement setup

        self.playerList = arcade.SpriteList()

        self.player = PlayerSprite(.5, "idle", 10, game_window=self, strength=3)
        self.player.position = 300, 300

        self.player.stand_right_textures = []
        self.player.stand_left_textures = []
        #stand right/left
        frame = arcade.load_texture(str(self.player_idle_ath), 0, 0, height=137, width=184)
        self.player.texture = frame
        self.player.stand_right_textures.append(frame)
        frame = arcade.load_texture(str(self.player_idle_ath), 0, 0, height=137, width=184, mirrored=True)
        self.player.stand_left_textures.append(frame)
        #walk right/left
        self.player.walk_right_textures = []
        self.player.walk_left_textures = []
        self.player.walk_up_textures = []
        self.player.walk_down_textures = []
        for image_num in range(7):
            frame = arcade.load_texture(str(self.player_run_path), image_num * 184, 0, height=125, width=184)
            self.player.walk_right_textures.append(frame)
            self.player.walk_up_textures.append(frame)
        for image_num in range(7):
            frame = arcade.load_texture(str(self.player_run_path), image_num * 184, 0, height=125, width=184, mirrored=True)
            self.player.walk_left_textures.append(frame)
            self.player.walk_down_textures.append(frame)
        self.playerList.append(self.player)
        # end player movement

        # enemy setup - reg skull
        self.firstEnemy = arcade.Sprite(str(self.skull_animation), scale=1, image_width=54, image_height=70,
                                        center_x=150, center_y=450)
        self.enemyList.append(self.firstEnemy)

        self.secondEnemy = arcade.Sprite(str(self.skull_animation), scale=1, image_width=54, image_height=70,
                                        center_x=450, center_y=450)
        self.enemyList.append(self.secondEnemy)

        self.thirdEnemy = arcade.Sprite(str(self.skull_animation), scale=1, image_width=54, image_height=70,
                                         center_x=150, center_y=150)
        self.enemyList.append(self.thirdEnemy)

        self.fourthEnemy = arcade.Sprite(str(self.skull_animation), scale=1, image_width=54, image_height=70,
                                        center_x=450, center_y=150)
        self.enemyList.append(self.fourthEnemy)
        self.simple_Physics = arcade.PhysicsEngineSimple(self.player, self.flood_walls_list)

    def move_enemy(self):
       # print(self.firstEnemy.center_x)

            self.firstEnemy.change_x += 5

        #    self.firstEnemy.change_x -= 5

    def intro(self):
        """displays life points"""
        output = f"Player Life points: " + str(self.player.life) + f"\nPlayer Strength points:" + str(
            self.player.strength) + f"\nKill Score:" + str(self.kill_score)
        arcade.draw_lrtb_rectangle_filled(0, 170, 600, 550, arcade.color.WARM_BLACK)
        arcade.draw_text(output, 0, 555, arcade.color.WHITE_SMOKE, 13)

    def spawn_strength_coin(self, img_path, x, y):

        strength_coin_Path = pathlib.Path.cwd() / 'Assets' / img_path

        self.strengthCoin = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
        coin_frames = []
        for col in range(8):
            frame = arcade.load_texture(str(strength_coin_Path), x=col*32, y=0, height=32, width=32)
            coin_frames.append(frame)
        self.strengthCoin.textures = coin_frames
        self.strCoinList.append(self.strengthCoin)


    """
    def check_for_map_change(self):
        collision = False
        for tile in self.doorlist:
            # check each door tile to see if the player is touching it.
            if collision:
                # change to the next map
                self.current_map += 1
                # if on map 2, change all spritelists

                self.floorlist = arcade.tilemap.process_layer(self.outdoors_map, "Grass", 1)
                self.wallslist = arcade.tilemap.process_layer(self.outdoors_map, "Wall", 1)
                self.doorlist = arcade.tilemap.process_layer(self.outdoors_map, "Doors", 1)
                self.bedlist = arcade.tilemap.process_layer(self.outdoors_map, "Extra Wall", 1)
                self.other1 = None
                self.other2 = None
                #Update enemyList
                '''Add enemies here'''
                #change player's location
                '''change player.center_x and player.center_y'''
    """
    def on_key_press(self, key: int, modifiers: int):
        """ Movement"""
        if key == arcade.key.LEFT:
            self.player_direction = "left"
            self.player.change_x = -PLYR_MOVE_SPEED
            print(self.player.center_x,", ", self.player.center_y)
        elif key == arcade.key.RIGHT:
            self.player_direction = "right"
            self.player.change_x = PLYR_MOVE_SPEED
            print(self.player.center_x, ", ", self.player.center_y)
        elif key == arcade.key.UP:
            self.player.change_y = PLYR_MOVE_SPEED
            print(self.player.center_x, ", ", self.player.center_y)
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLYR_MOVE_SPEED
            print(self.player.center_x, ", ", self.player.center_y)


        if key == arcade.key.SPACE:
            arcade.play_sound(self.player_sword_sound)
            self.player.state = "attacking"
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

        """
        self.floorlist.draw()
        self.wallslist.draw()
        self.wallslist.draw()
        self.doorlist.draw()
        self.bedlist.draw()
        """

        self.flood_grass_list.draw()
        self.flood_walls_list.draw()
        self.strCoinList.draw()
        self.enemyList.draw()
        self.playerList.draw()
        self.intro()

#        self.other1.draw()
 #       self.other2.draw()


        # self.other1.draw()
        #self.other2.draw()


    def check_for_collision(self):
        if arcade.check_for_collision_with_list(self.player, self.doorlist):
            #if we are on map1:
            self.current_map += 1




    def on_update(self, delta_time: float):

        self.frame_count += 1
      #  print(self.frame_count)

        self.playerList.update()
        self.playerList.update_animation()

        self.strCoinList.update()
        self.strCoinList.update_animation()
        self.enemyList.update()

        self.simple_Physics.update()
        #self.move_enemy()

        # ATK ENEMY
        for enemy in self.enemyList:
            skull_atk = arcade.check_for_collision_with_list(self.player, self.enemyList)
            if len(skull_atk) > 0 and self.player.state == "attacking" :
                arcade.play_sound(self.skull_death)
                self.kill_score +=1
                enemy.kill()

        # PICK UP COIN
        # ADDS  TO STR VAL
        for self.strengthCoin in self.strCoinList:
            items_touched = arcade.check_for_collision_with_list(self.strengthCoin, self.playerList)
            if len(items_touched) > 0:
                self.strengthCoin.kill()
                arcade.play_sound(self.coin_sound)
                self.player.strength += 1
                self.player_inventory.append(self.strengthCoin)


def main():
    """The Main Method"""
    window = MultiLayeredWindow()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
