import arcade

# From arcade online docs
from entity import Entity
from entityManager import EntityManager
from eventManager import EventManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from transform import Transform


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def __create_player(self):
        # Setup player
        # Create an arcade.Sprite for the player
        player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5)
        player_sprite.center_x = 50
        player_sprite.center_y = 64
        # Create a sprite renderer component
        player_sprite_renderer = SpriteRenderer(player_sprite)
        # Create a transform component for the player
        player_transform = Transform((50, 500), 12, (1.0, 1.0))
        # Create player controller component
        player_controller = PlayerController()
        # Create physics component for the player
        player_physics = PhysicsObject(uses_gravity=True, max_velocity=(500, 500))
        # Create the player entity and add all the components to it
        player_entity = Entity("Player", ["PlayerTag"],
                               [player_sprite_renderer, player_transform, player_controller, player_physics])
        # Add the player entity to the manager
        EntityManager.add_entity(player_entity)

    def setup(self):
        self.__create_player()
        #self.__create_level()

        arcade.set_background_color(arcade.color.AMAZON)

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
        EntityManager.draw()


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN_TITLE = "ONI x MATSURI"

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    window.run()


if __name__ == '__main__':
    main()
