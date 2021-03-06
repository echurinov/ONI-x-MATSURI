# Equivalent to Unity's GameObject
# Entities have Components, which give them functionality
# Entities can be tagged to help find them
class Entity:
    def __init__(self, name="", tags=[], components=[], static=False, active=True):
        self.__name = name
        self.__tags = tags
        self.__components = components
        for item in components:
            item.parent = self  # Set the parent of each component to this entity
        self.__static = static  # Whether this entity is static. Decides which spritelist the entity is put into
        self.__children = []
        self.__parent = None
        self.__active = active
        self.__transform = None
        self.in_scene = False  # Used to know who to send events to
        # Call on_added_to_entity and on_created on all child components
        for item in components:
            if hasattr(item, 'on_added_to_entity'):
                item.on_added_to_entity()
            if hasattr(item, 'on_created'):
                item.on_created()

    # Add a component to an entity
    def add_component(self, component):
        self.__components.append(component)
        component.parent = self
        if hasattr(component, 'on_added_to_entity'):
            component.on_added_to_entity()

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.__active = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    # TODO: this will search for no reason if the entity has no transform component
    # Nearly all entities have them, but this will be slow on entities that don't
    @property
    def transform(self):
        if self.__transform is None:
            self.__transform = self.get_component_by_name("Transform")
        return self.__transform

    # Adds an entity as a child of this entity
    def add_child(self, entity):
        self.__children.append(entity)
        entity.parent = self

    # Returns the first component matching the given name,
    # or None if the entity doesn't have this component
    def get_component_by_name(self, name):
        for component in self.__components:
            if name == component.name:
                return component
        return None

    @property
    def components(self):
        return self.__components

    @property
    def static(self):
        return self.__static

    @static.setter
    def static(self, value):
        self.__static = value

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, value):
        self.__tags = value

