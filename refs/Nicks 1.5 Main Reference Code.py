import arcade
import pathlib
import random
from enum import auto, Enum

# CONSTANTS

PLAYER_SPEED = 5
BULLET_SPEED = 10
GRAVITY = 1
JUMP_SPEED = 15

LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

MAX_ENEMIES_ON_SCREEN = 5
SCORE_TO_GET_ENEMY_2 = 45


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed: int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window

    def move(self, list: arcade.SpriteList, direction: MoveEnum):
        # as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP:
            for thing in list:
                if self.top >= thing.bottom:
                    pass
                else:
                    self.center_y += PLAYER_SPEED
            print(self.center_x, self.center_y)
        elif direction == MoveEnum.DOWN:
            self.center_y -= PLAYER_SPEED
            print(self.center_x, self.center_y)
        elif direction == MoveEnum.LEFT:
            self.center_x -= PLAYER_SPEED
            print(self.center_x, self.center_y)
        elif direction == MoveEnum.RIGHT:
            self.center_x += PLAYER_SPEED
            print(self.center_x, self.center_y)
        else:  # should be MoveEnum.NONE
            pass


def move(sprite: arcade.Sprite, slist: arcade.SpriteList, direction: MoveEnum):
    # as a class exercise, lets fix this so it doesn't go off the window
    if direction == MoveEnum.UP:
        sprite.center_y += PLAYER_SPEED
        print("Top: " + str(sprite.top) +
              "\nBottom: " + str(sprite.bottom) +
              "\nLeft: " + str(sprite.left) +
              "\nRight: " + str(sprite.right))

    elif direction == MoveEnum.DOWN:
        if sprite.bottom > 63.0:
            sprite.center_y -= PLAYER_SPEED
        else:
            pass
        print("Top: " + str(sprite.top) +
              "\nBottom: " + str(sprite.bottom) +
              "\nLeft: " + str(sprite.left) +
              "\nRight: " + str(sprite.right))
    elif direction == MoveEnum.LEFT:
        sprite.center_x -= PLAYER_SPEED
        print("Top: " + str(sprite.top) +

              "\nBottom: " + str(sprite.bottom) +

              "\nLeft: " + str(sprite.left) +

              "\nRight: " + str(sprite.right))
    elif direction == MoveEnum.RIGHT:
        sprite.center_x += PLAYER_SPEED
        print("Top: " + str(sprite.top) +
              "\nBottom: " + str(sprite.bottom) +
              "\nLeft: " + str(sprite.left) +
              "\nRight: " + str(sprite.right))
    else:  # should be MoveEnum.NONE
        pass


class MinimalArcade(arcade.Window):

    def __init__(self, image_name: str, screen_w: int = 1024, screen_h: int = 750):
        super().__init__(screen_w, screen_h)
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.pict = None
        self.direction = MoveEnum.NONE
        self.pictlist = None

    def setup(self):
        self.pict = MinimalSprite(str(self.image_path), speed=5, game_window=self)
        self.pict.center_x = 500
        self.pict.center_y = 500
        self.pictlist = arcade.SpriteList()
        self.pictlist.append(self.pict)

    def on_update(self, delta_time: float):
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        self.pict.move(self.direction)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        self.pictlist.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT

    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and \
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.LEFT or key == arcade.key.A) and \
                self.direction == MoveEnum.LEFT:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.RIGHT or key == arcade.key.D) and \
                self.direction == MoveEnum.RIGHT:
            self.direction = MoveEnum.NONE


class ArcadeButWithStuff(arcade.Window):

    def __init__(self, screen_w: int = 1024, screen_h: int = 500):

        super().__init__(screen_w, screen_h)

        self.bullet_list = None
        self.wall_list = None
        self.obstacle_list = None
        self.player_list = None
        self.enemy_list = None
        self.enemy_bullet_list = None

        self.player_sprite = None
        self.direction = MoveEnum.NONE
        self.physics_engine = None
        self.player_is_shooting = False
        self.shot_sound = None
        self.enemy_shot_sound = None
        self.enemy_hit_sound = None
        self.player_hit_sound = None
        self.game_over = None
        self.win = None
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

        '''self.map_image_path = pathlib.Path.cwd() / 'Assets' / image_names[0]
        self.player_image_path = pathlib.Path.cwd() / 'Assets' / image_names[1]
        self.bullet_image_path = pathlib.Path.cwd() / 'Assets' / image_names[2]
        self.map_pict = None
        self.player_pict = None
        self.bullet_pict = None
        self.direction = MoveEnum.NONE
        self.pictlist = None '''

    def setup(self):
        # Create the Sprite Lists
        self.frame_count = 0
        self.enemies_on_map = 1

        self.shot_sound = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / "Yeet.wav")
        self.enemy_shot_sound = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / "EnemyMagic.wav")
        self.enemy_hit_sound = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / "EnemyHit.wav")
        self.player_hit_sound = None
        self.game_over = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / "Game Over.wav")
        self.win = arcade.load_sound(pathlib.Path.cwd() / 'Assets' / "Win.wav")
        self.score = 0
        self.player_dead = False

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        # set the player at its coordinates
        self.player_sprite = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "PlayerSprite1.png")
        self.player_sprite.center_x = 10
        self.player_sprite.center_y = 95
        self.player_list.append(self.player_sprite)

        # set initial enemy position
        self.enemy_sprite = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "Enemy1.png")
        self.enemy_sprite.center_x = 269
        self.enemy_sprite.center_y = 95
        self.enemy_list.append(self.enemy_sprite)

        # Create the ground
        for i in range(-200, 5000, 64):
            wall = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'Tiles' / "GrassUpDirt.png")
            wall.center_x = i
            wall.center_y = 32
            self.wall_list.append(wall)

        # add a few rocks
        coordinate_list = [[512, 96], [768, 96], [934, 96], [2000, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'Tiles' / "rock.png")
            wall.position = coordinate
            self.obstacle_list.append(wall)

        # add the enemy spawn points
        spawnpoint_list = [[4100, 96], [2905, 96], [1420, 96], [1720, 96], [333, 96]]
        for coordinate in spawnpoint_list:
            wall = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'Tiles' / "enemyspawnpoint.png")
            wall.position = coordinate
            self.obstacle_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_update(self, delta_time: float):

        self.frame_count += 1
        print(self.frame_count)

        x_coordinates = [333.0, 1420.0, 1720.0, 2905.0, 4100.0]

        if self.frame_count % 240 == 0 and self.enemies_on_map < 10:
            random.seed(1)
            self.spawn_enemy(random.choices(x_coordinates))
            random.seed(1)


        # If the current frame divided by 360 has a remainder of 0, have the enemy shoot
        if self.frame_count % 360 == 0 and self.player_dead == False:
            self.enemy_shoot()
        for eb in self.enemy_bullet_list:
            if self.player_dead == True:
                arcade.draw_text("Game Over...", 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)
                if self.frame_count % 200:
                    arcade.close_window()
            for wall in self.obstacle_list:
                if arcade.check_for_collision(eb, wall):
                    eb.remove_from_sprite_lists()
                    eb.kill
                if arcade.check_for_collision(eb, self.player_sprite):
                    eb.remove_from_sprite_lists()
                    eb.kill
                    self.player_sprite.remove_from_sprite_lists()
                    self.player_sprite.kill
                    self.player_dead = True
                    arcade.play_sound(self.game_over)
                    break

                    # self.score += 1
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        move(self.player_sprite, self.wall_list, self.direction)
        self.bullet_list.update()
        self.enemy_list.update()
        self.enemy_bullet_list.update()
        for bullet in self.bullet_list:
            for wall in self.obstacle_list:
                if arcade.check_for_collision(bullet, wall):
                    bullet.remove_from_sprite_lists()
                    bullet.kill
                    # wall.remove_from_sprite_lists()
                    # self.score += 1

            for enemy in self.enemy_list:
                if arcade.check_for_collision(bullet, enemy):
                    enemy.remove_from_sprite_lists()
                    arcade.play_sound(self.enemy_hit_sound)
                    if self.score < 450:
                        enemy.kill
                        enemy.remove_from_sprite_lists
                        self.enemies_on_map -=1
                    bullet.remove_from_sprite_lists
                    bullet.kill
                    self.score += 10
                if arcade.check_for_collision(enemy, self.player_sprite):
                    arcade.play_sound(self.game_over)
                    self.player_sprite.remove_from_sprite_lists()
                    self.player_sprite.kill
                    frame_of_death = self.frame_count
                    if self.frame_count >= frame_of_death + 200:
                        arcade.close_window()

            '''if bullet.bottom > self.height or bullet.top < 0:
                bullet.kill()
            if bullet.center_x > self.width or bullet.center_x < 0:
                bullet.kill()'''
        # Scroll Logic
        changed = False
        # Scroll to the Left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll to the Right
        right_boundary = self.view_left + self.width - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # FREEZE

        # EVERYBODY CLAP YO HANDS

        # Scroll up
        top_boundary = self.view_bottom + self.height - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left, self.width + self.view_left, self.view_bottom, self.height +
                                self.view_bottom)

        # self.player_sprite.move(self.direction)

        if self.score >= 600:
            self.player_dead = True
            arcade.play_sound(self.win)
            for enemy in self.enemy_list:
                enemy.remove_from_sprite_lists
            self.player_sprite.remove_from_sprite_lists
            for bullet in self.bullet_list:
                bullet.remove_from_sprite_lists
            for bullet in self. enemy_bullet_list:
                bullet.remove_from_sprite_lists
            arcade.set_background_color(arcade.csscolor.BLACK)
            arcade.draw_text("Game Over...", 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)


    def spawn_enemy(self, x):

        if self.score <= 450:
            enemy_sprite = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "Enemy1.png")
            enemy_sprite.center_x = random.randint(128, 5000)
            enemy_sprite.center_y = 95
            self.enemy_list.append(self.enemy_sprite)
        else:
            enemy_sprite = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "Enemy2.png")
            enemy_sprite.center_x = (x)
            enemy_sprite.center_y = 95
            self.enemy_list.append(self.enemy_sprite)



    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here
        if not self.player_dead:
            self.wall_list.draw()
            self.obstacle_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.enemy_list.draw()
            self.enemy_bullet_list.draw()
            score_text = f"Score: {self.score}"
            arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)
        else:
            arcade.set_background_color(arcade.csscolor.BLACK)
            arcade.draw_text("Game Over...", 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)

    def enemy_shoot(self):
        for enemy in self.enemy_list:
            # arcade.sound.play_sound(self.enemy_shot_sound)
            bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "enemy magic (bullet).png")
            # If the enemy is to the left of the player
            if enemy.center_x < self.player_sprite.center_x:
                bullet.change_x = BULLET_SPEED
                bullet.center_x = enemy.center_x + 32
                bullet.center_y = enemy.center_y + 16
                self.enemy_bullet_list.append(bullet)
                arcade.sound.play_sound(self.enemy_shot_sound)

            elif enemy.center_x > self.player_sprite.center_x:
                bullet.angle = 180
                bullet.change_x = -BULLET_SPEED
                bullet.center_x = enemy.center_x - 32
                bullet.center_y = enemy.center_y + 16
                self.enemy_bullet_list.append(bullet)
                arcade.sound.play_sound(self.enemy_shot_sound)

    def shoot(self):

        arcade.sound.play_sound(self.shot_sound)

        bullet = arcade.Sprite(pathlib.Path.cwd() / 'Assets' / "TestBullet.png")

        if self.direction == MoveEnum.UP:
            bullet.angle = 90
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y + 32

        if self.direction == MoveEnum.DOWN:
            bullet.angle = 270
            bullet.change_y = -BULLET_SPEED
            self.bullet_list.append(bullet)
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y - 32

        if self.direction == MoveEnum.LEFT:
            bullet.angle = 180
            bullet.change_x = -BULLET_SPEED
            self.bullet_list.append(bullet)
            bullet.center_x = self.player_sprite.center_x - 32
            bullet.center_y = self.player_sprite.center_y

        if self.direction == MoveEnum.RIGHT:
            bullet.change_x = BULLET_SPEED
            self.bullet_list.append(bullet)
            bullet.center_x = self.player_sprite.center_x + 32
            bullet.center_y = self.player_sprite.center_y

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.direction = MoveEnum.LEFT
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.direction = MoveEnum.RIGHT
        elif key == arcade.key.SPACE:
            self.shoot()

    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and \
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.LEFT or key == arcade.key.A) and \
                self.direction == MoveEnum.LEFT:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.RIGHT or key == arcade.key.D) and \
                self.direction == MoveEnum.RIGHT:
            self.direction = MoveEnum.NONE


def main():
    """ Main method
    player = MinimalSprite(pathlib.Path.cwd() / 'Assets' / 'PlayerSprite1.png')
    test_map = MinimalSprite(pathlib.Path.cwd() / 'Assets' / 'TestMap.png')
    bullet = MinimalSprite(pathlib.Path.cwd() / 'Assets' / 'Bullet')    """

    window = ArcadeButWithStuff(screen_h=920, screen_w=1080)

    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
