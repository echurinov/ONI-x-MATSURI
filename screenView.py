import random

import arcade

from backgroundResizer import BackgroundResizer
from collider import Collider
from enemyController import EnemyController
from entity import Entity
from gameManager import GameManager
from eventManager import EventManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from transform import Transform
import mapSections


class StartView(arcade.View):
    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.texture = arcade.load_texture("assets/backgrounds/start_screen.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width - 1, 0, self.window.height - 1)

    def on_draw(self):
        # Draw this view
        self.clear()
        self.texture.draw_sized(GameManager.SCREEN_WIDTH / 2, GameManager.SCREEN_HEIGHT / 2, GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def __create_level(self):
        # Setup level

        # Create box entities for a somewhat random floor

        entities = mapSections.section1()
        for i in entities:
            GameManager.add_entity(i)

        # Create entities for background (tiled)
        for i in range(10):
            background_sprite = arcade.Sprite("assets/backgrounds/oni_background.png", 1.0)
            background_sprite_renderer = SpriteRenderer(background_sprite)
            background_transform = Transform((i * background_sprite.width, background_sprite.height / 2), 0, (1.0, 1.0))
            background_resizer = BackgroundResizer()
            background_entity = Entity("Background", ["BackgroundTag"],
                                       [background_sprite_renderer, background_transform, background_resizer])
            GameManager.add_background_entity(background_entity)

    def __create_player(self):
        # Setup player
        # Create an arcade.Sprite for the player
        player_sprite = arcade.Sprite("assets/sprites/player/player_idle_1.png")
        # Create a sprite renderer component
        player_sprite_renderer = SpriteRenderer(player_sprite)
        # Create a transform component for the player
        player_transform = Transform((50, 1000), 0, (1.0, 1.0))
        # Create player controller component
        player_controller = PlayerController()
        # Create a collider component for the player (Will autogenerate hitbox when entity is created)
        player_collider = Collider(auto_generate_polygon="box")
        # Create the player entity and add all the components to it
        player_entity = Entity("Player", ["Player"],
                               [player_sprite_renderer, player_transform, player_controller, player_collider],
                               static=False)
        # Add the player entity to the manager
        GameManager.add_entity(player_entity)

    def __create_enemy(self, xy_position):
        # Setup enemy(Red Oni)
        # Create an arcade.Sprite for the enemy(Red Oni)
        enemy_sprite = arcade.Sprite("assets/sprites/enemy/oni_idle_1.png")
        # Create a sprite renderer component
        enemy_sprite_renderer = SpriteRenderer(enemy_sprite)
        # Create a transform component for the enemy
        enemy_transform = Transform(xy_position, 0, (1.0, 1.0))
        # Create enemy controller component
        enemy_controller = EnemyController()
        # Create a collider component for the enemy (Will autogenerate hitbox when entity is created)
        enemy_collider = Collider(auto_generate_polygon="box")
        # Create the enemy entity and add all the components to it
        enemy_entity = Entity("Enemy", ["Enemy"],
                               [enemy_sprite_renderer, enemy_transform, enemy_controller, enemy_collider],
                               static=False)
        # Add the enemy entity to the manager
        GameManager.add_entity(enemy_entity)

    def setup(self):
        self.__create_player()
        self.__create_level()
        self.__create_enemy((300, 266))
        self.__create_enemy((600, 266))
        self.__create_enemy((800, 266))
        arcade.set_background_color(arcade.color_from_hex_string("#172040"))

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


