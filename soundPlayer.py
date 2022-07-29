import arcade
import pyglet

# This class bundles the arcade.Sound and pyglet.media.player.Player classes to handle stopping sounds
# A pyglet.media.player.Player created from an arcade.Sound is needed to stop the arcade.Sound
# This can be used to stop sounds currently playing when switching scenes (e.g., Stopping a Boss attack sound on Player death when displaying LoseView)

class SoundPlayer:
    def __init__(self, sound: arcade.Sound, player: pyglet.media.player.Player):
        self.__sound = sound
        self.__player = player

    @property
    def player(self):
        return self.__player

    @property
    def sound(self):
        return self.__sound