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
        self.__static = static
        self.__children = []
        self.__parent = None
        self.__active = active
        # Call on_added_to_entity on all child components
        for item in components:
            if hasattr(item, 'on_added_to_entity'):
                item.on_added_to_entity()

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

    # Adds an entity as a child of this entity
    def add_child(self, entity):
        self.__children.append(entity)
        entity.parent = self

    # Returns the first component matching the given name,
    # or None if the entity doesn't have this component
    def get_component_by_name(self, name):
        for index, component in enumerate(self.__components):
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
