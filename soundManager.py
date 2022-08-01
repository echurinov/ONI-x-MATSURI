import arcade
import time

from eventManager import EventManager
from gameManager import GameManager
from soundPlayer import SoundPlayer

SOUND_VOLUME = 1.0
SOUND_PATH = "assets/sounds/"

# Handles all loading and playing of sounds
# Centralizes sound loading into 1 class
# Everything in this class is static


class SoundManager:
    # Stores SoundPlayer objects
    __active_sounds = []
    # __sound_lists will store the pre-loaded sounds
    # This class will create a pyglet.media.player.Player when play_sound() is invoked
    __sound_lists = {
        "enemy_oni" : {
            "damage": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_damage_2.wav"),
            "death": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_death.wav")
        },
        "enemy_oni_boss" : {

        },
        "player" : {
            "attack" : arcade.load_sound(SOUND_PATH + "player/player_attack.wav"),
            "damage" : arcade.load_sound(SOUND_PATH + "player/player_damage.wav"),
            "jump" : arcade.load_sound(SOUND_PATH + "player/player_jump3.wav")
        },
        "powerups" : {
            "heal" : arcade.load_sound(SOUND_PATH + "powerups/cotton_candy.wav")
        },
        "user_interface" : {
            "start_button_press" : arcade.load_sound(SOUND_PATH + "menu/button_press2.wav"),
            "quit_button_press" : arcade.load_sound(SOUND_PATH + "menu/button_press.wav")
        }
    }

    @staticmethod
    def play_sound(domain: str, sound_name: str, sound_volume = SOUND_VOLUME):
        sound = SoundManager.__sound_lists[domain][sound_name]
        player = arcade.play_sound(sound, sound_volume)
        sound_player = SoundPlayer(sound, player)
        SoundManager.__active_sounds.append(sound_player)
    
    @staticmethod
    def test_play_sound(relative_file_path: str):
        sound = arcade.load_sound(relative_file_path)
        player = arcade.play_sound(sound)
        sound_player = SoundPlayer(sound, player)
        SoundManager.__active_sounds.append(sound_player)

    @staticmethod
    def stop_active_sounds():
        if SoundManager.__active_sounds is None:
            return
        for sound_player in SoundManager.__active_sounds:
            # Hacky workaround for crash. This should never be None but it is sometimes
            if sound_player.player is None:
                continue
            sound_player.sound.stop(sound_player.player)

    def __on_update(self):
        if SoundManager.__active_sounds is None:
            return
        # Remove sounds that have finished playing
        list_copy = SoundManager.__active_sounds
        for sound_player in list_copy:
            # Hacky workaround for crash
            if sound_player.player is None:
                continue
            if sound_player.sound.get_stream_position(sound_player.player) == 0.0:
                SoundManager.__active_sounds.remove(sound_player)

    @staticmethod
    def start():
        # Updates used to monitor if played sounds have finished playing
        EventManager.add_listener("Update", SoundManager.__on_update)
