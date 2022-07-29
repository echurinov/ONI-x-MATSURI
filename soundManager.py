import arcade
import time

from eventManager import EventManager
from gameManager import GameManager
from soundPlayer import SoundPlayer, sound

SOUND_VOLUME = 1.0
SOUND_PATH = "assets/sounds/"

# Handles all loading and playing of sounds
# Centralizes sound loading into 1 class
# Everything in this class is static


class SoundManager:
    __active_sounds = []
    # __sound_lists will store the pre-loaded sounds
    # This class will create a pyglet.media.player.Player when play_sound() is invoked
    __sound_lists = {
        "player" : {},
        "enemy_oni" : {},
        "enemy_oni_boss" : {},
        "user_interface" : {}
    }

    @staticmethod
    def play_sound(domain: str, sound_name: str, sound_volume = SOUND_VOLUME):
        sound = SoundManager.__sound_lists[domain][sound_name]
        player = arcade.play_sound(sound)
        sound_player = SoundPlayer(sound, player)
        SoundManager.__active_sounds.append(sound_player)

    @staticmethod
    def stop_active_sounds():
        if SoundManager.__active_sounds is None:
            return
        for sound_player in SoundManager.__active_sounds:
            sound_player.sound.stop(sound_player.player)

    def __on_update(self):
        if self.__active_sounds is None:
            return
        # Remove sounds that have finished playing
        for sound_player in self.__active_sounds:
            if sound_player.get_stream_position(sound_player.player) == 0.0:
                self.__active_sounds.remove(sound_player)

    @staticmethod
    def start():
        #Load sounds
        #Player
        player_attack_sound = arcade.load_sound(SOUND_PATH + "player/player_attack.wav")
        player_damage_sound = arcade.load_sound(SOUND_PATH + "player/player_damage.wav")
        player_jump_sound = arcade.load_sound(SOUND_PATH + "player/player_jump3.wav")

        #Enemy Oni
        enemy_oni_damage_sound = arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_damage_2.wav")
        enemy_oni_death_sound = arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_death.wav")

        #Enemy Oni Boss

        #User Interface
        start_button_press_sound = arcade.load_sound(SOUND_PATH + "menu/button_press2.wav")
        quit_button_press_sound = arcade.load_sound(SOUND_PATH + "menu/button_press.wav")

        #Create players for each sound
        #Player
        player_attack_sound = arcade.load_sound(SOUND_PATH + "player/player_attack.wav")
        player_damage_sound = arcade.load_sound(SOUND_PATH + "player/player_damage.wav")
        player_jump_sound = arcade.load_sound(SOUND_PATH + "player/player_jump3.wav")

        #Enemy Oni
        enemy_oni_damage_sound = arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_damage_2.wav")
        enemy_oni_death_sound = arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_death.wav")

        #Enemy Oni Boss

        #User Interface
        start_button_press_sound = arcade.load_sound(SOUND_PATH + "menu/button_press2.wav")
        quit_button_press_sound = arcade.load_sound(SOUND_PATH + "menu/button_press.wav")

        # Updates used to check if played sounds have finished playing, remove from __active_sounds
        EventManager.add_listener("Update", SoundManager.__on_update)
