import arcade


# Handles all the entities in the game
# Everything in this class is static
class EntityManager:
    __entities = []
    # Setup sprite lists for drawing stuff to the screen
    __dynamic_entities = arcade.SpriteList()
    __static_entities = arcade.SpriteList()

    @staticmethod
    def get_dynamic_entities():
        return EntityManager.__dynamic_entities

    @staticmethod
    def get_static_entities():
        return EntityManager.__static_entities

    # Adds a new entity.
    # Handles adding it to sprite lists so it gets rendered
    @staticmethod
    def add_entity(entity):
        EntityManager.__entities.append(entity)
        sprite = entity.get_component_by_name("SpriteRenderer")
        # Only add to sprite lists if entity has a sprite component
        if sprite is not None:
            if entity.static:
                EntityManager.__static_entities.append(sprite.sprite)
            else:
                EntityManager.__dynamic_entities.append(sprite.sprite)
        # Call on_created for all components attached to this entity
        for component in entity.components:
            if hasattr(component, 'on_created'):
                component.on_created()

    # Returns a list of entities matching the given name
    @staticmethod
    def get_entities_by_name(name):
        to_return = []
        for item in EntityManager.__entities:
            if item.name == name:
                to_return.append(item)
        return to_return

    # Returns a list of active collider components in the scene
    @staticmethod
    def get_colliders():
        colliders = []
        for entity in EntityManager.__entities:
            if entity.active:
                collider = entity.get_component_by_name("Collider")
                if collider is not None:
                    colliders.append(collider)
        return colliders

    # Draw everything to screen
    @staticmethod
    def draw():
        EntityManager.__dynamic_entities.draw()
        EntityManager.__static_entities.draw()

        # Debug
        if True:
            for collider in EntityManager.get_colliders():
                arcade.draw_polygon_outline(collider.polygon, arcade.color.RED, 2)
            string_to_print = "Pos: " + str(EntityManager.get_entities_by_name("Player")[0].get_component_by_name("Transform").position)
            string_to_print2 = "Touching ground: " + str(EntityManager.get_entities_by_name("Player")[0].get_component_by_name("PhysicsObject").touching_ground)
            arcade.draw_text(string_to_print, 0, 500, arcade.color.BLACK, 20)
            arcade.draw_text(string_to_print2, 0, 470, arcade.color.BLACK, 20)
