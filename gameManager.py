import arcade


# Handles all the entities in the game and drawing them
# Everything in this class is static
from collider import Collider


class GameManager:
    __entities = []
    # Setup sprite lists for drawing stuff to the screen
    __dynamic_entities_spritelist = arcade.SpriteList()
    __static_entities_spritelist = arcade.SpriteList()
    __background_entities_spritelist = arcade.SpriteList()
    __gui_entities_spritelist = arcade.SpriteList()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    debug = False

    __paused = False

    @staticmethod
    def get_paused():
        return GameManager.__paused

    @staticmethod
    def set_paused(value):
        GameManager.__paused = value
        if value:
            print("Paused")
        else:
            print("Unpaused")

    main_camera = None  # Scrolling camera
    gui_camera = None  # Static camera

    # Delta time, here for convenience
    dt = 0.02

    # Runs once the game is started and the window is created
    @staticmethod
    def start():
        width, height = arcade.window_commands.get_display_size()
        GameManager.main_camera = arcade.Camera(width, height)
        GameManager.gui_camera = arcade.Camera(width, height)
        GameManager.set_paused(False)

    @staticmethod
    def get_dynamic_entities():
        return GameManager.__dynamic_entities_spritelist

    @staticmethod
    def get_static_entities():
        return GameManager.__static_entities_spritelist

    @staticmethod
    def get_background_entities():
        return GameManager.__background_entities_spritelist

    @staticmethod
    def get_gui_entities():
        return GameManager.__gui_entities_spritelist

    @staticmethod
    def remove_tagged_entities(tag):
        for entity in GameManager.__entities:
            if tag in entity.tags:
                for component in entity.components:
                    if hasattr(component, "on_remove"):
                        component.on_remove()
                if hasattr(entity, "on_remove"):
                    entity.on_remove()
                GameManager.__entities.remove(entity)
                entity.in_scene = False
                if entity.get_component_by_name("SpriteRenderer"):
                    sprite = entity.get_component_by_name("SpriteRenderer").sprite
                    if sprite in GameManager.__static_entities_spritelist:
                        GameManager.__static_entities_spritelist.remove(sprite)
                    if sprite in GameManager.__dynamic_entities_spritelist:
                        GameManager.__dynamic_entities_spritelist.remove(sprite)
                    if sprite in GameManager.__background_entities_spritelist:
                        GameManager.__background_entities_spritelist.remove(sprite)
                    if sprite in GameManager.__gui_entities_spritelist:
                        GameManager.__gui_entities_spritelist.remove(sprite)
                else:
                    print("Entity", entity.name, "has no SpriteRenderer")

    @staticmethod
    def remove_all_entities():
        for entity in GameManager.__entities:
            for component in entity.components:
                if hasattr(component, "on_remove"):
                    component.on_remove()
            if hasattr(entity, "on_remove"):
                entity.on_remove()
        GameManager.__entities = []
        GameManager.__dynamic_entities_spritelist = arcade.SpriteList()
        GameManager.__static_entities_spritelist = arcade.SpriteList()
        GameManager.__background_entities_spritelist = arcade.SpriteList()
        GameManager.__gui_entities_spritelist = arcade.SpriteList()

    @staticmethod
    def remove_background_entities():
        for entity in GameManager.__entities:
            if entity.get_component_by_name("SpriteRenderer"):
                sprite = entity.get_component_by_name("SpriteRenderer").sprite
                if sprite in GameManager.__background_entities_spritelist:
                    GameManager.__background_entities_spritelist.remove(sprite)
                    GameManager.remove_entity(entity)
        GameManager.__background_entities_spritelist = arcade.SpriteList()  # Clear the spritelist

    @staticmethod
    def remove_static_entities():
        for entity in GameManager.__entities:
            if entity.get_component_by_name("SpriteRenderer"):
                sprite = entity.get_component_by_name("SpriteRenderer").sprite
                if sprite in GameManager.__static_entities_spritelist:
                    GameManager.__static_entities_spritelist.remove(sprite)
                    GameManager.remove_entity(entity)
        GameManager.__static_entities_spritelist.clear()

    @staticmethod
    def remove_entity(entity):
        entity.in_scene = False
        if entity in GameManager.__entities:
            GameManager.__entities.remove(entity)
            for component in entity.components:
                if hasattr(component, "on_remove"):
                    component.on_remove()
            if hasattr(entity, "on_remove"):
                entity.on_remove()
        else:
            #print("Entity", entity.name, "not found in GameManager.__entities")
            pass

        if entity.get_component_by_name("SpriteRenderer"):
            sprite = entity.get_component_by_name("SpriteRenderer").sprite
            if sprite in GameManager.__static_entities_spritelist:
                GameManager.__static_entities_spritelist.remove(sprite)
            if sprite in GameManager.__dynamic_entities_spritelist:
                GameManager.__dynamic_entities_spritelist.remove(sprite)
            if sprite in GameManager.__background_entities_spritelist:
                GameManager.__background_entities_spritelist.remove(sprite)
            if sprite in GameManager.__gui_entities_spritelist:
                GameManager.__gui_entities_spritelist.remove(sprite)
        else:
            print("Entity", entity.name, "has no SpriteRenderer")

    # Adds a background entity (draws below everything else, has no collision)
    @staticmethod
    def add_background_entity(entity):
        entity.in_scene = True
        GameManager.__entities.append(entity)
        # Add sprite to list so it gets drawn
        sprite = entity.get_component_by_name("SpriteRenderer")
        if sprite is not None:
            GameManager.__background_entities_spritelist.append(sprite.sprite)
        # Call on_created for all components attached to this entity
        for component in entity.components:
            if hasattr(component, 'on_created'):
                component.on_created()
        # Call on_created on the entity if it has it (behaviour should be in components, but whatever)
        if hasattr(entity, "on_created"):
            entity.on_created()

    # Adds a new entity.
    # Handles adding it to sprite lists so it gets rendered
    @staticmethod
    def add_entity(entity):
        entity.in_scene = True
        GameManager.__entities.append(entity)
        sprite = entity.get_component_by_name("SpriteRenderer")
        # Only add to sprite lists if entity has a sprite component
        if sprite is not None:
            if entity.static:
                GameManager.__static_entities_spritelist.append(sprite.sprite)
            else:
                GameManager.__dynamic_entities_spritelist.append(sprite.sprite)
        # Call on_created for all components attached to this entity
        for component in entity.components:
            if hasattr(component, 'on_created'):
                component.on_created()
        # Call on_created on the entity if it has it (behaviour should be in components, but whatever)
        if hasattr(entity, "on_created"):
            entity.on_created()

    # Adds a new GUI entity.
    # Handles adding it to sprite lists so it gets rendered
    @staticmethod
    def add_gui_entity(entity):
        entity.in_scene = True
        GameManager.__entities.append(entity)
        sprite = entity.get_component_by_name("SpriteRenderer")
        # Only add to sprite lists if entity has a sprite component
        if sprite is not None:
            GameManager.__gui_entities_spritelist.append(sprite.sprite)
        # Call on_created for all components attached to this entity
        for component in entity.components:
            if hasattr(component, 'on_created'):
                component.on_created()
        # Call on_created on the entity if it has it (behaviour should be in components, but whatever)
        if hasattr(entity, "on_created"):
            entity.on_created()

    # Sets an entity to be static (True) or dynamic (False) and assigns it to the relevant SpriteList
    @staticmethod
    def set_static(entity, static):
        sprite = entity.get_component_by_name("SpriteRenderer")
        if sprite is not None:
            # Remove entity from existing sprite lists
            if entity.static:
                GameManager.__static_entities_spritelist.remove(sprite.sprite)
            else:
                GameManager.__dynamic_entities_spritelist.remove(sprite.sprite)
            # Add entity to new sprite list
            if static:
                GameManager.__static_entities_spritelist.append(sprite.sprite)
            else:
                GameManager.__dynamic_entities_spritelist.append(sprite.sprite)
        # Set the static flag if it isn't already set
        entity.static = static

    # Returns a list of entities with a given tag
    @staticmethod
    def get_entities_by_tag(tag):
        to_return = []
        for item in GameManager.__entities:
            if tag in item.tags:
                to_return.append(item)
        return to_return

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

    # Returns a list of all entities
    @staticmethod
    def get_entities():
        return GameManager.__entities

    # Clears gui sprites for redraw
    @staticmethod
    def clear_gui_sprite():
        GameManager.__gui_entities_spritelist.clear()

    # Draw everything to screen
    @staticmethod
    def draw():
        GameManager.main_camera.use()
        GameManager.__background_entities_spritelist.draw()
        GameManager.__static_entities_spritelist.draw()
        GameManager.__dynamic_entities_spritelist.draw()
        # Debug
        if GameManager.debug:
            for collider in GameManager.get_colliders():
                if collider.auto_generate_polygon == "box":
                    arcade.draw_rectangle_outline(collider.transform.position[0], collider.transform.position[1], collider.width, collider.height, arcade.color.RED, 2)
                else:
                    arcade.draw_polygon_outline(collider.polygon, arcade.color.RED, 2)
                arcade.draw_circle_outline(collider.transform.position[0], collider.transform.position[1], 5.0, arcade.color.GREEN)

        # Draw GUI
        GameManager.gui_camera.use()
        GameManager.__gui_entities_spritelist.draw()

        # Debug
        if GameManager.debug:
            #player_cont = GameManager.get_entities_by_name("Player")[0].get_component_by_name("PlayerController")
            #string_to_print = "Pos: " + str(GameManager.get_entities_by_name("Player")[0].get_component_by_name("Transform").position)
            #string_to_print2 = "Vel: " + str(player_cont.velocity)

            #arcade.draw_text(string_to_print, 0, 500, arcade.color.BLACK, 20, anchor_x="left", anchor_y="bottom")
            #arcade.draw_text(string_to_print2, 0, 470, arcade.color.BLACK, 20, anchor_x="left", anchor_y="bottom")
            arcade.draw_text("Frame time: " + str(GameManager.dt), 0, 530, arcade.color.BLACK, 20, anchor_x="left", anchor_y="bottom")
            arcade.draw_text(str(len(GameManager.get_entities())) + " entities", 0, 550, arcade.color.BLACK, 20, anchor_x="left", anchor_y="bottom")
