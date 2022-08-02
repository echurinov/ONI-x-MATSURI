import arcade


# This class is used to manage all the entities in the game.
# All methods and variables are static
# Examples of events are Update, which is triggered every frame
class EventManager:

    __listeners = {}

    # Add a listener for an event to the event manager
    # When this event is triggered, all listeners will be called
    @staticmethod
    def add_listener(event_name, method):
        if event_name not in EventManager.__listeners:
            EventManager.__listeners[event_name] = []
        EventManager.__listeners[event_name].append(method)

    # Remove a listener from an event
    @staticmethod
    def remove_listener(event_name, method):
        if event_name in EventManager.__listeners and method in EventManager.__listeners[event_name]:
            EventManager.__listeners[event_name].remove(method)

    # Trigger an event
    # When this function is run, all listeners for this event will be called and passed *args
    @staticmethod
    def trigger_event(event_name, *args):
        if event_name in EventManager.__listeners:
            for method in EventManager.__listeners[event_name]:
                method(*args)

    # Remove all listeners for an event
    @staticmethod
    def clear_listeners(event_name):
        if event_name in EventManager.__listeners:
            EventManager.__listeners[event_name] = []