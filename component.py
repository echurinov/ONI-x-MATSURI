
# Abstract class for Components
# All Components must inherit from this class
class Component:
    def __init__(self, name):
        self.__name = name
        self.__parent = None

    @property
    def name(self):
        return self.__name

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value
