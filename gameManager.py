import arcade


# Handles all the entities in the game and drawing them
# Everything in this class is static
from collider import Collider


class GameManager:
    __entities = []
    # Setup sprite lists for drawing stuff to the screen
    __dynamic_entities = arcade.SpriteList()
    __static_entities = arcade.SpriteList()
    __background_entities = arcade.SpriteList()
    __gui_entities = arcade.SpriteList()

    __scroll_position = (0, 0)

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    main_camera = None # Scrolling camera
    gui_camera = None # Static camera

    # Runs once the game is started and the window is created
    @staticmethod
    def start():
        GameManager.main_camera = arcade.Camera(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT)
        GameManager.gui_camera = arcade.Camera(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT)

    @staticmethod
    def get_dynamic_entities():
        return GameManager.__dynamic_entities

    @staticmethod
    def get_static_entities():
        return GameManager.__static_entities

    @staticmethod
    def get_background_entities():
        return GameManager.__background_entities


    # Adds a new entity.
    # Handles adding it to sprite lists so it gets rendered
    @staticmethod
    def add_entity(entity):
        GameManager.__entities.append(entity)
        sprite = entity.get_component_by_name("SpriteRenderer")
        # Only add to sprite lists if entity has a sprite component
        if sprite is not None:
            if entity.static:
                GameManager.__static_entities.append(sprite.sprite)
            else:
                GameManager.__dynamic_entities.append(sprite.sprite)
        # Call on_created for all components attached to this entity
        for component in entity.components:
            if hasattr(component, 'on_created'):
                component.on_created()

    # Sets an entity to be static (True) or dynamic (False) and assigns it to the relevant SpriteList
    @staticmethod
    def set_static(entity, static):
        sprite = entity.get_component_by_name("SpriteRenderer")
        if sprite is not None:
            # Remove entity from existing sprite lists
            if entity.static:
                GameManager.__static_entities.remove(sprite.sprite)
            else:
                GameManager.__dynamic_entities.remove(sprite.sprite)
            # Add entity to new sprite list
            if static:
                GameManager.__static_entities.append(sprite.sprite)
            else:
                GameManager.__dynamic_entities.append(sprite.sprite)
        # Set the static flag if it isn't already set
        entity.static = static

    # Returns a list of entities matching the given name
    @staticmethod
    def get_entities_by_name(name):
        to_return = []
        for item in GameManager.__entities:
            if item.name == name:
                to_return.append(item)
        return to_return

    # Returns a list of active collider components in the scene
    @staticmethod
    def get_colliders():
        colliders = []
        for entity in GameManager.__entities:
            if entity.active:
                collider = entity.get_component_by_name("Collider")
                if collider is not None:
                    colliders.append(collider)
        return colliders

    # Draw everything to screen
    @staticmethod
    def draw():
        GameManager.main_camera.use()
        GameManager.__background_entities.draw()
        GameManager.__static_entities.draw()
        GameManager.__dynamic_entities.draw()
        # Debug
        if True:
            for collider in GameManager.get_colliders():
                arcade.draw_polygon_outline(Collider.translate_polygon(collider.polygon, (
                -GameManager.__scroll_position[0], -GameManager.__scroll_position[1])), arcade.color.RED, 2)

        # Draw GUI
        GameManager.gui_camera.use()
        GameManager.__gui_entities.draw()

        # Debug
        if True:
            string_to_print = "Pos: " + str(GameManager.get_entities_by_name("Player")[0].get_component_by_name("Transform").position)
            string_to_print2 = "Touching ground: " + str(GameManager.get_entities_by_name("Player")[0].get_component_by_name("PhysicsObject").touching_ground)
            arcade.draw_text(string_to_print, 0, 500, arcade.color.BLACK, 20)
            arcade.draw_text(string_to_print2, 0, 470, arcade.color.BLACK, 20)

    @staticmethod
    def get_scroll():
        return GameManager.__scroll_position

    @staticmethod
    def set_scroll(scroll):
        GameManager.__scroll_position = (scroll[0], scroll[1])
        # Update each entity's position based on the scroll position
        for entity in GameManager.__entities:
            transform = entity.get_component_by_name("Transform")
            transform.position = transform.position

    @staticmethod
    def scroll_screen(scroll):
        GameManager.__scroll_position = (GameManager.__scroll_position[0] + scroll[0], GameManager.__scroll_position[1] + scroll[1])
        # Update each entity's position based on the scroll position
        for entity in GameManager.__entities:
            transform = entity.get_component_by_name("Transform")
            transform.position = transform.position
