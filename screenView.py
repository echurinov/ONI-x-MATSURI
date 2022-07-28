"""Background music taken from https://api.arcade.academy/en/2.5.7/examples/background_music.html"""

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
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from swordController import SwordController
from transform import Transform
import mapSections

#Default volume of all songs played in-game
MUSIC_VOLUME = 0.5


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

        # Set up variable to manage music for the GameView
        self.__music_list = []
        self.__current_song_index = 0
        self.__current_player = None
        self.__music = None

    def __create_level(self):
        # Setup level

        # Create box entities for a somewhat random floor

        entities = mapSections.load_from_file("level.dat")
        #entities = mapSections.section3()
        for i in entities:
            GameManager.add_entity(i)

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
        for i in range(3):
            heart_sprite = arcade.Sprite("assets/sprites/heart_full.png", 1.0)
            heart_sprite_renderer = SpriteRenderer(heart_sprite)
            heart_transform = Transform((i * (heart_sprite.width + 10) + 70, 750 + heart_sprite.height / 2), 0, 1.0)
            heart_entity = Entity("Heart", ["HeartTag"], [heart_sprite_renderer, heart_transform])
            GameManager.add_gui_entity(heart_entity)

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
        # Create the player entity and add all the components to it
        player_entity = Entity("Player", ["Player"],
                               [player_sprite_renderer, player_transform, self.player_controller, player_collider],
                               static=False)
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
        sword_attack_sprite = arcade.Sprite(":resources:onscreen_controls/flat_dark/select.png", scale=3, image_height=48, image_width=80)
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
    
    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.__current_song_index += 1
        if self.__current_song_index >= len(self.__music_list):
            self.__current_song_index = 0
        print(f"Advancing song to {self.__current_song_index}.")

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        self.stop_song()

        # Play the next song
        print(f"Playing {self.__music_list[self.__current_song_index]}")
        self.__music = arcade.Sound(self.__music_list[self.__current_song_index], streaming=True)
        self.__current_player = self.__music.play(MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def stop_song(self):
        if self.__music:
            self.__music.stop(self.__current_player)

    def setup(self):
        self.__create_player()
        self.__create_level()
        self.__create_sword()
        arcade.set_background_color(arcade.color_from_hex_string("#172040"))

        # List of music
        self.__music_list = ["assets/sounds/music/main_stage_music.mp3"]
        # Array index of what to play
        self.__current_song_index = 0
        # Play the song
        self.play_song()

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

        position = self.__music.get_stream_position(self.__current_player)
        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()

        # Wait for game over
        if GameManager.get_entities_by_tag("Player")[0].get_component_by_name("PlayerController").health == 0:
            lose_view = LoseView()
            self.stop_song()
            self.window.show_view(lose_view)

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
        if 1417 < x < 1505 and 750 < y < 842:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        # DOESN'T WORK AND IDK HOW TO MAKE IT
        if 1417 < x < 1505 and 750 < y < 842:
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

        # Probably don't want this song to loop since it's short (?)
        # Not fully set up like the background music in GameView
        self.__lose_music = arcade.load_sound("assets/sounds/music/J 3ds3 24 Btl Lose 3ds.mp3")

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
        arcade.play_sound(self.__lose_music)

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
        self.press_sound = arcade.load_sound("assets/sounds/menu/button_press2.wav")

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        if not self.__start_pressed:
            arcade.play_sound(self.press_sound)
            self.__start_pressed = True
            game_view = GameView()
            game_view.setup()
            self.View.window.show_view(game_view)


class QuitButton(arcade.gui.UITextureButton):
    def __init__(self, *args, **keywords):
        super().__init__(**keywords)
        self.__start_pressed = False
        self.press_sound = arcade.load_sound("assets/sounds/menu/button_press.wav")

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("Quitting")
        arcade.play_sound(self.press_sound)
        arcade.exit()


class ReturnButton(arcade.gui.UITextureButton):
    def __init__(self, current_view: arcade.View, *args, **keywords):
        super().__init__(**keywords)
        self.View = current_view
        self.__start_pressed = False

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start_view = StartView()
        #start_view.setup()
        self.View.window.show_view(start_view)

