import arcade

# From arcade online docs
from collider import Collider
from entity import Entity
from gameManager import GameManager
from eventManager import EventManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from transform import Transform


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def __create_level(self):
        # Setup level
        # Create sprite for platform
        level_sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png")
        # Create sprite renderer component
        level_sprite_renderer = SpriteRenderer(level_sprite)
        # Create transform component
        level_transform = Transform((100, 100), 0, (1.0, 1.0))
        # Create collider (hitbox will be generated when entity is created)
        level_collider = Collider()
        # Create platform entity and add all the components to it
        level_entity = Entity("Level", ["LevelTag"], [level_sprite_renderer, level_transform, level_collider],
                              static=True)
        # Add the platform entity to the manager
        GameManager.add_entity(level_entity)

    def __create_player(self):
        # Setup player
        # Create an arcade.Sprite for the player
        player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png")
        # Create a sprite renderer component
        player_sprite_renderer = SpriteRenderer(player_sprite)
        # Create a transform component for the player
        player_transform = Transform((50, 500), 0, (1.0, 1.0))
        # Create player controller component
        player_controller = PlayerController()
        # Create physics component for the player
        player_physics = PhysicsObject(uses_gravity=True, max_velocity=(5000, 5000))
        # Create a collider component for the player (Will autogenerate hitbox when entity is created)
        player_collider = Collider()
        # Create the player entity and add all the components to it
        player_entity = Entity("Player", ["PlayerTag"],
                               [player_sprite_renderer, player_transform, player_controller, player_physics,
                                player_collider],
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
        EventManager.trigger_event("PhysicsUpdate", dt)
        EventManager.trigger_event("GravityUpdate", -9.8, dt)

    def on_key_press(self, key, modifiers):
        # Trigger key press events
        EventManager.trigger_event("KeyPress", key, modifiers)

    def on_key_release(self, key, modifiers):
        # Trigger key release events
        EventManager.trigger_event("KeyRelease", key, modifiers)

    def on_draw(self):
        # Render the screen
        self.clear()
        GameManager.draw()


def main():
    SCREEN_TITLE = "ONI x MATSURI"

    window = MyGame(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
