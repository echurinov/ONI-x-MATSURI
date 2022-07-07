import random

import arcade

from backgroundResizer import BackgroundResizer
from collider import Collider
from entity import Entity
from gameManager import GameManager
from eventManager import EventManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from transform import Transform


class StartView(arcade.View):
    def on_show_view(self):
        #This is run once when we switch to this view
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        # Draw this view
        self.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def __create_level(self):
        # Setup level

        # Create box entities for a somewhat random floor
        for i in range(100):
            # Create sprite for platform
            level_sprite = random.choice((arcade.Sprite("assets/tiles/box1.png", 0.25),
                                          arcade.Sprite("assets/tiles/box2.png", 0.25)))
            # Create sprite renderer component
            level_sprite_renderer = SpriteRenderer(level_sprite)
            # Create transform component
            level_transform = Transform((i * 100 * random.uniform(0.5, 1), 100 + random.uniform(-50, 50)), 0,
                                        (1.0, 1.0))
            # Create collider (hitbox will be generated when entity is created)
            level_collider = Collider(auto_generate_polygon="box")
            # Create platform entity and add all the components to it
            level_entity = Entity("Block " + str(i), ["Ground"], [level_sprite_renderer, level_transform, level_collider],
                                  static=True)
            # Add the platform entity to the manager
            GameManager.add_entity(level_entity)

        # Create platform entities
        for i in range(30):
            # Create sprite for platform
            platform_sprite = random.choice((arcade.Sprite("assets/tiles/platform1.png", 0.25),
                                             arcade.Sprite("assets/tiles/platform2.png", 0.25)))
            # Create sprite renderer component
            platform_sprite_renderer = SpriteRenderer(platform_sprite)
            # Create transform component
            platform_transform = Transform((i * 200 * random.uniform(0.25, 1.75), 400 + random.uniform(-50, 50)), 0,
                                           (1.0, 1.0))
            # Create collider (hitbox will be generated when entity is created)
            platform_collider = Collider(auto_generate_polygon="box")
            # Create platform entity and add all the components to it
            platform_entity = Entity("Level", ["Platform"],
                                     [platform_sprite_renderer, platform_transform, platform_collider],
                                     static=True)
            # Add the platform entity to the manager
            GameManager.add_entity(platform_entity)

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
        player_sprite = arcade.Sprite("assets/sprites/player/player_idle_1.png", 0.5)
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

    def setup(self):
        self.__create_player()
        self.__create_level()
        arcade.set_background_color(arcade.color.AMAZON)

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


