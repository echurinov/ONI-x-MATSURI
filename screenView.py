import random

import arcade

import arcade.gui

import time

from backgroundResizer import BackgroundResizer
from collider import Collider
from enemyController import EnemyController
from entity import Entity
from gameManager import GameManager
from eventManager import EventManager
from levelSectionLoader import LevelSectionLoader
from musicManager import MusicManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from soundManager import SoundManager
from spriteRenderer import SpriteRenderer
from swordController import SwordController
from transform import Transform
import mapSections


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        # Create managers and box for buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        box = arcade.gui.UIBoxLayout(x=0, y=0, vertical=False)
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x='center_x', anchor_y='center_y', child=box))

        # Start button
        button = StartButton(self, x=0, y=0, texture=arcade.load_texture('assets/sprites/start_button.png'),
                                            texture_hovered=arcade.load_texture('assets/sprites/start_button_highlighted.png'),
                                            texture_pressed=arcade.load_texture('assets/sprites/start_button_pressed.png'))
        box.add(button.with_space_around(right=20, top=100))

        # Quit Button
        quit_button = QuitButton(x=0, y=0, texture=arcade.load_texture('assets/sprites/quit_button.png'),
                                            texture_hovered=arcade.load_texture('assets/sprites/quit_button_highlighted.png'),
                                            texture_pressed=arcade.load_texture('assets/sprites/quit_button_pressed.png'))
        box.add(quit_button.with_space_around(left=20, top=100))

    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Load background
        background_sprite = arcade.Sprite("assets/backgrounds/start_screen.png", 1.0)
        background_sprite_renderer = SpriteRenderer(background_sprite)
        background_transform = Transform((background_sprite.width / 2, background_sprite.height / 2), 0, 1.0)
        background_resizer = BackgroundResizer()
        background_entity = Entity("Background", ["BackgroundTag"],
                                   [background_sprite_renderer, background_transform, background_resizer])
        GameManager.add_background_entity(background_entity)

        # Shouldn't need this, but it won't resize otherwise for some reason
        background_resizer.on_resize(self.window.width, self.window.height)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        # arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        # Draw this view
        self.clear()
        GameManager.draw()
        self.manager.draw()

    #def on_mouse_press(self, _x, _y, _button, _modifiers):
    #    """ If the user presses the mouse button, start the game. """
    #    game_view = GameView()
    #    game_view.setup()
    #    self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def __create_level(self):
        # Setup level

        # Create box entities for a somewhat random floor

        #level_length, entities = mapSections.load_from_file("level.dat")
        #entities = mapSections.section3()
        #print("Loaded level with", len(entities), "entities and length", level_length)
        #for i in entities:
        #    GameManager.add_entity(i)

        # Create entities for background (tiled)
        for i in range(10):
            background_sprite = arcade.Sprite("assets/backgrounds/oni_background.png", 1.0)
            background_sprite_renderer = SpriteRenderer(background_sprite)
            background_transform = Transform((i * background_sprite.width, background_sprite.height / 2), 0, 1.0)
            background_resizer = BackgroundResizer()
            background_entity = Entity("Background", ["BackgroundTag"],
                                       [background_sprite_renderer, background_transform, background_resizer])
            GameManager.add_background_entity(background_entity)

        # Create heart sprites
        # Heart sprites are handled in the player controller now
        #for i in range(3):
        #    heart_sprite = arcade.Sprite("assets/sprites/heart_full.png", 1.0)
        #    heart_sprite_renderer = SpriteRenderer(heart_sprite)
        #    heart_transform = Transform((i * (heart_sprite.width + 10) + 70, 750 + heart_sprite.height / 2), 0, 1.0)
        #    heart_entity = Entity("Heart", ["HeartTag"], [heart_sprite_renderer, heart_transform])
        #    GameManager.add_gui_entity(heart_entity)

    def __create_player(self):
        # Setup player
        # Create an arcade.Sprite for the player
        player_sprite = arcade.Sprite("assets/sprites/player/player_idle_1.png")
        # Create a sprite renderer component
        player_sprite_renderer = SpriteRenderer(player_sprite)
        # Create a transform component for the player
        player_transform = Transform((50, 1000), 0, 1.0)
        # Create player controller component
        self.player_controller = PlayerController()
        # Create a collider component for the player (Will autogenerate hitbox when entity is created)
        player_collider = Collider(auto_generate_polygon="box")
        # Create a level section loader component for the player. This handles loading the level sections
        level_section_loader = LevelSectionLoader()
        # Create the player entity and add all the components to it
        player_entity = Entity("Player", ["Player"],
                               [player_sprite_renderer, player_transform, self.player_controller, player_collider,
                                level_section_loader], static=False)
        # Add the player entity to the manager
        GameManager.add_entity(player_entity)

        #Create a sword entity
        #sword_transform = Transform((500,500), 0, (0.5, 0.5))
        #sword_controller = PlayerController()
        #sword_collider = Collider(auto_generate_polygon="box")

        #GameManager.add_entity(sword_entity)

    def __create_sword(self):
        # Create an arcade.Sprite for the sword (it will be invisible, so it doesn't matter what it is)
        # Using a rectangle that covers the player character and extends in front
        sword_attack_sprite = arcade.Sprite(":resources:onscreen_controls/flat_dark/select.png", scale=3, image_height=48, image_width=40)
        # Set the texture to be invisible
        sword_attack_sprite.alpha = 0
        # Create a sprite renderer component for the sword
        sword_attack_sprite_renderer = SpriteRenderer(sword_attack_sprite)
        # Create a transform component for the sword
        sword_attack_transform = Transform((200, 110), 0, 1.0)
        # Create sword controller component
        sword_attack_controller = SwordController()
        # Create a collider component for the sword (Will autogenerate hitbox when entity is created)
        sword_attack_collider = Collider(auto_generate_polygon="box")
        # Create the sword entity and add all the components to it
        sword_attack_entity = Entity("Sword", ["Sword"],
                               [sword_attack_sprite_renderer, sword_attack_transform, sword_attack_controller, sword_attack_collider],
                               static=False)
        # Add the sword entity to the manager
        GameManager.add_entity(sword_attack_entity)

    def setup(self):
        self.__create_player()
        self.__create_level()
        self.__create_sword()
        arcade.set_background_color(arcade.color_from_hex_string("#172040"))

        MusicManager.change_list("game_view")
        MusicManager.play_song()
        # Trigger the "Start" event
        EventManager.trigger_event("Start")

    def on_update(self, dt):
        # Trigger screen update event
        EventManager.trigger_event("Update", dt)

        # Don't do physics or gravity if we're paused
        if GameManager.get_paused():
            return
        EventManager.trigger_event("PhysicsUpdate", dt)
        EventManager.trigger_event("GravityUpdate", -9.8, dt)

        # Wait for game over
        if GameManager.get_entities_by_tag("Player")[0].get_component_by_name("PlayerController").health == 0:
            MusicManager.stop_song()
            self.begin_boss()
            GameManager.get_entities_by_tag("Player")[0].get_component_by_name("PlayerController").health = 5
            #lose_view = LoseView()
            #SoundManager.stop_active_sounds()
            #MusicManager.change_list("lose_view", loop=False)
            #MusicManager.play_song()
            #self.window.show_view(lose_view)

    def begin_boss(self):
        # Remove all entities except Player elements and GUI
        GameManager.remove_background_entities()
        GameManager.remove_static_entities()

        enemy_entities = GameManager.get_entities_by_tag("Enemy")
        for obj in enemy_entities:
            GameManager.remove_entity(obj)

        power_entities = GameManager.get_entities_by_tag("PowerUp")
        for obj in power_entities:
            GameManager.remove_entity(obj)

        # Reset player position
        self.player_controller.set_transform((50, 1000))

        # Set up new level layout
        # Background
        background_sprite = arcade.Sprite("assets/backgrounds/boss_background.png", 1.0)
        background_sprite_renderer = SpriteRenderer(background_sprite)
        background_transform = Transform((background_sprite.width / 2, background_sprite.height / 2), 0, 1.0)
        background_resizer = BackgroundResizer()
        background_entity = Entity("Background", ["BackgroundTag"],
                                   [background_sprite_renderer, background_transform, background_resizer])
        GameManager.add_background_entity(background_entity)

        # Invisible floor collider
        floor_sprite = arcade.Sprite("assets/sprites/boss_ground.png")
        floor_sprite_renderer = SpriteRenderer(floor_sprite)
        floor_transform = Transform((floor_sprite.width / 2, floor_sprite.height / 2), 0, 1.0)
        floor_collider = Collider(auto_generate_polygon="simple")
        ground_entity = Entity("Ground", ["GroundTag"], [floor_sprite_renderer, floor_transform, floor_collider],
                                          static=True)
        GameManager.add_entity(ground_entity)

        # Create boss

        # Reset and freeze camera
        GameManager.main_camera.move((0, 0))
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.player_controller.toggle_camera_movement()

        # Change music
        MusicManager.change_list("boss_view")
        MusicManager.play_song()

    def on_key_press(self, key, modifiers):
        # Don't do anything if we're paused
        if GameManager.get_paused():
            return
        # Trigger key press events
        EventManager.trigger_event("KeyPress", key, modifiers)

    def on_key_release(self, key, modifiers):
        # Don't do anything if we're paused
        if GameManager.get_paused():
            return
        # Trigger key release events
        EventManager.trigger_event("KeyRelease", key, modifiers)

    def on_draw(self):
        # Render the screen
        self.clear()
        GameManager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if 1816 < x < 1904 and 976 < y < 1044:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        if 1816 < x < 1904 and 976 < y < 1044:
            self.player_controller.set_exit_sprite(arcade.Sprite("assets/sprites/exit_highlighted.png", 1.0))
        else:
            self.player_controller.set_exit_sprite(arcade.Sprite("assets/sprites/exit.png", 1.0))


class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        # Create managers and box for buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        box = arcade.gui.UIBoxLayout(x=0, y=0, vertical=False)
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x='center_x', anchor_y='center_y', child=box))

        # Return button
        button = StartButton(self, x=0, y=0, texture=arcade.load_texture('assets/sprites/return_button.png'),
                                            texture_hovered=arcade.load_texture('assets/sprites/return_button_highlighted.png'),
                                            texture_pressed=arcade.load_texture('assets/sprites/return_button_pressed.png'))
        box.add(button.with_space_around(top=100))


    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Load background
        background_sprite = arcade.Sprite("assets/backgrounds/win_screen.png", 1.0)
        background_sprite_renderer = SpriteRenderer(background_sprite)
        background_transform = Transform((background_sprite.width / 2, background_sprite.height / 2), 0, 1.0)
        background_resizer = BackgroundResizer()
        background_entity = Entity("Background", ["BackgroundTag"],
                                   [background_sprite_renderer, background_transform, background_resizer])
        GameManager.add_background_entity(background_entity)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        # Draw this view
        self.clear()
        GameManager.draw()
        self.manager.draw()


class LoseView(arcade.View):
    def __init__(self):
        super().__init__()
        # Create managers and box for buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        box = arcade.gui.UIBoxLayout(x=0, y=0, vertical=False)
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x='center_x', anchor_y='center_y', child=box))

        # Return button
        button = ReturnButton(self, x=0, y=0, texture=arcade.load_texture('assets/sprites/return_button.png'),
                                            texture_hovered=arcade.load_texture('assets/sprites/return_button_highlighted.png'),
                                            texture_pressed=arcade.load_texture('assets/sprites/return_button_pressed.png'))
        box.add(button.with_space_around(top=450, right=50))

    def on_show_view(self):
        """ This is run once when we switch to this view """
        GameManager.remove_all_entities()

        # Load background
        background_sprite = arcade.Sprite("assets/backgrounds/lose_screen.png", 1.0)
        background_sprite_renderer = SpriteRenderer(background_sprite)
        background_transform = Transform((background_sprite.width / 2, background_sprite.height / 2), 0, 1.0)
        background_resizer = BackgroundResizer()
        background_entity = Entity("Background", ["BackgroundTag"],
                                   [background_sprite_renderer, background_transform, background_resizer])
        GameManager.add_background_entity(background_entity)

        background_resizer.on_resize(self.window.width, self.window.height)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        GameManager.main_camera.move((0, 0))

    def on_draw(self):
        # Draw this view
        self.clear()
        GameManager.draw()
        self.manager.draw()


class StartButton(arcade.gui.UITextureButton):
    def __init__(self, current_view: arcade.View, *args, **keywords):
        super().__init__(**keywords)
        self.View = current_view
        self.__start_pressed = False

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        if not self.__start_pressed:
            SoundManager.play_sound("user_interface", "start_button_press")
            self.__start_pressed = True
            game_view = GameView()
            game_view.setup()
            self.View.window.show_view(game_view)


class QuitButton(arcade.gui.UITextureButton):
    def __init__(self, *args, **keywords):
        super().__init__(**keywords)
        self.__start_pressed = False

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("Quitting")
        SoundManager.play_sound("user_interface", "quit_button_press")
        arcade.exit()


class ReturnButton(arcade.gui.UITextureButton):
    def __init__(self, current_view: arcade.View, *args, **keywords):
        super().__init__(**keywords)
        self.View = current_view
        self.__start_pressed = False

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start_view = StartView()
        #start_view.setup()
        MusicManager.change_list("start_view")
        MusicManager.play_song()
        self.View.window.show_view(start_view)

