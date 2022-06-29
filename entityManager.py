import arcade


# Handles all the entities in the game
# Everything in this class is static
class EntityManager:
    __entities = []
    # Setup sprite lists for drawing stuff to the screen
    __dynamic_entities = arcade.SpriteList()
    __static_entities = arcade.SpriteList()

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

    # Draw everything to screen
    @staticmethod
    def draw():
        EntityManager.__dynamic_entities.draw()
        EntityManager.__static_entities.draw()
