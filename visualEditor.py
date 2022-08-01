import copy
import os

import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Visual Editor"


def myround(x, base=5, grid_offset=0):
    return base * round(float(x) / base) + grid_offset


def round_camera_to_world(x, base, camera_pos, world_camera_pos):
    return myround(x, base)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.mouse_sprite = arcade.Sprite(":resources:onscreen_controls/shaded_light/unchecked.png", 0.125)
        self.background_sprite = arcade.Sprite("assets/backgrounds/oni_background.png", 1.0)
        self.background_sprite.center_x = self.background_sprite.width / 2
        self.background_sprite.center_y = self.background_sprite.height / 2

        self.static_sprite_list = arcade.SpriteList()
        self.gui_sprite_list = arcade.SpriteList()
        self.gui_sprite_list.append(self.mouse_sprite)
        self.drawer_sprite_list = arcade.SpriteList()

        self.main_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.drawer_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.grabbed_sprite = None
        self.grid_size = 32
        self.grid_offset = (0, 0)
        self.point_grid = []
        self.drawer_open = False
        self.scroll_amount = 0

        self.details_open = False
        self.detail_position = (0, 0)

        self.keys = {
            arcade.key.A: False,
            arcade.key.D: False,
            arcade.key.W: False,
            arcade.key.S: False,
            arcade.key.LSHIFT: False,
            arcade.key.RSHIFT: False
        }

        for i in range(-75, 75):
            self.point_grid.append((i * self.grid_size + self.grid_offset[0], -SCREEN_HEIGHT * 5 + self.grid_offset[1]))
            self.point_grid.append((i * self.grid_size + self.grid_offset[0], SCREEN_HEIGHT * 5 + self.grid_offset[1]))

        for i in range(-75, 75):
            self.point_grid.append((-SCREEN_WIDTH * 5 + self.grid_offset[0], i * self.grid_size + self.grid_offset[1]))
            self.point_grid.append((SCREEN_WIDTH * 5 +  self.grid_offset[0], i * self.grid_size + self.grid_offset[1]))

    def open_details(self, sprite):
        self.details_open = True
        self.detail_position = (sprite.center_x, sprite.center_y)

    # Returns the length of the level
    # Length is measured from the left edge of the leftmost sprite to the right edge of the rightmost sprite
    def get_level_length(self):
        left_sprite = None
        right_sprite = None
        for sprite in self.static_sprite_list:
            if left_sprite is None or sprite.center_x < left_sprite.center_x:
                left_sprite = sprite
            if right_sprite is None or sprite.center_x > right_sprite.center_x:
                right_sprite = sprite
        left_pos = left_sprite.center_x - left_sprite.width / 2
        right_pos = right_sprite.center_x + right_sprite.width / 2
        return right_pos - left_pos

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        if symbol == arcade.key.F:
            self.drawer_open = not self.drawer_open
        self.keys[symbol] = True

        # Save
        if symbol == arcade.key.P:
            with open("level.dat", "w") as file:
                file.write(str(self.get_level_length()) + "\n")
                for sprite in self.static_sprite_list:
                    file.write(sprite.name + ":" + str(sprite.center_x) + ":" + str(sprite.center_y) + ":" + str(sprite.scale) +"\n" )
        # Load
        if symbol == arcade.key.O:
            with open("level.dat", "r") as file:
                self.static_sprite_list = arcade.SpriteList()
                for index, line in enumerate(file):
                    if index == 0:  # Ignore length line
                        continue
                    name, x, y, scale = line.split(":")
                    sprite = arcade.Sprite("assets/visual_editor_sprites/" + name, float(scale))
                    sprite.name = name
                    sprite.center_x = float(x)
                    sprite.center_y = float(y)
                    self.static_sprite_list.append(sprite)

    def on_key_release(self, symbol: int, modifiers: int):
        self.keys[symbol] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_sprite.center_x = x
        self.mouse_sprite.center_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Clicked")
            self.mouse_sprite.center_x += self.drawer_camera.position[0]
            self.mouse_sprite.center_y += self.drawer_camera.position[1]
            collisions = arcade.check_for_collision_with_list(self.mouse_sprite, self.drawer_sprite_list, method=2)
            self.mouse_sprite.center_x -= self.drawer_camera.position[0]
            self.mouse_sprite.center_y -= self.drawer_camera.position[1]
            if len(collisions) > 0:
                print("Grabbed")
                self.grabbed_sprite = copy.deepcopy(collisions[0])
                self.grabbed_sprite.scale = 1.0
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            print("Right Clicked")
            self.mouse_sprite.center_x += self.main_camera.position[0]
            self.mouse_sprite.center_y += self.main_camera.position[1]
            collisions = arcade.check_for_collision_with_list(self.mouse_sprite, self.static_sprite_list, method=2)
            self.mouse_sprite.center_x -= self.main_camera.position[0]
            self.mouse_sprite.center_y -= self.main_camera.position[1]
            if len(collisions) > 0:
                print("Deleting", collisions[0].name)
                self.static_sprite_list.remove(collisions[0])

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        print("Dropped")
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.grabbed_sprite is None:
            return

        self.grabbed_sprite.center_x = x + self.main_camera.position[0]
        self.grabbed_sprite.center_y = y + self.main_camera.position[1]
        if not (self.keys[arcade.key.LSHIFT] or self.keys[arcade.key.RSHIFT]):
            self.grabbed_sprite.center_x = myround(self.grabbed_sprite.center_x, self.grid_size, self.grid_offset[0])
            self.grabbed_sprite.center_y = myround(self.grabbed_sprite.center_y, self.grid_size, self.grid_offset[1])

        # print("Dropped:", (self.grabbed_sprite.center_x, self.grabbed_sprite.center_y))
        self.static_sprite_list.append(copy.deepcopy(self.grabbed_sprite))
        self.grabbed_sprite = None

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if self.drawer_open:
            self.scroll_amount += scroll_y
            self.scroll_amount = arcade.clamp(self.scroll_amount, -41, 41)
            if -40 < self.scroll_amount < 40:
                for sprite in self.drawer_sprite_list:
                    sprite.center_y -= scroll_y * 25

    def setup(self):
        for index, path in enumerate(os.listdir("assets/visual_editor_sprites/")):
            block_sprite = arcade.Sprite("assets/visual_editor_sprites/" + path, scale=0.5)
            if block_sprite.width > 500:
                block_sprite.scale = 0.25
            block_sprite.center_x = -150 + 200 * (index % 2)
            block_sprite.center_y = 100 + 200 * (index // 2)
            block_sprite.name = path
            self.drawer_sprite_list.append(block_sprite)

    def on_update(self, delta_time: float):
        if self.grabbed_sprite is not None:
            self.grabbed_sprite.center_x = self.mouse_sprite.center_x
            self.grabbed_sprite.center_y = self.mouse_sprite.center_y

            self.grabbed_sprite.center_x += self.main_camera.position[0]
            self.grabbed_sprite.center_y += self.main_camera.position[1]

            if not (self.keys[arcade.key.LSHIFT] or self.keys[arcade.key.RSHIFT]):
                self.grabbed_sprite.center_x = myround(self.grabbed_sprite.center_x, self.grid_size, self.grid_offset[0])
                self.grabbed_sprite.center_y = myround(self.grabbed_sprite.center_y, self.grid_size, self.grid_offset[1])

        if self.drawer_open:
            self.drawer_camera.move_to((-300, 0), 0.25)
        else:
            self.drawer_camera.move_to((300, 0), 0.25)

        if self.keys[arcade.key.A]:
            self.main_camera.move_to((self.main_camera.position[0] - 30, self.main_camera.position[1]), 0.25)
        if self.keys[arcade.key.D]:
            self.main_camera.move_to((self.main_camera.position[0] + 30, self.main_camera.position[1]), 0.25)
        if self.keys[arcade.key.W]:
            self.main_camera.move_to((self.main_camera.position[0], self.main_camera.position[1] + 30), 0.25)
        if self.keys[arcade.key.S]:
            self.main_camera.move_to((self.main_camera.position[0], self.main_camera.position[1] - 30), 0.25)

    def on_draw(self):
        self.clear()

        self.main_camera.use()
        self.background_sprite.draw()
        arcade.draw_lines(self.point_grid, arcade.color.AMAZON, 2)
        self.static_sprite_list.draw()

        self.drawer_camera.use()
        arcade.draw_rectangle_filled(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT, (0, 0, 0, 128))
        self.drawer_sprite_list.draw()

        self.gui_camera.use()
        self.gui_sprite_list.draw()
        if self.grabbed_sprite is not None:
            self.main_camera.use()
            self.grabbed_sprite.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
