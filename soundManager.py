import arcade
import time

import pyglet

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
        "enemy_oni": {
            "damage": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_damage.wav"),
            "death": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_death.wav")
        },
        "enemy_oni_boss": {
            "damage": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_damage.wav"),
            "death": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_death.wav"),
            "death_vaporize": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_death_vaporize.wav"),
            "drop": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_drop.wav"),
            "drum-attack": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_drum-attack.wav"),
            "drum-charge": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_drum-charge.wav"),
            "laugh": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_laugh.wav"),
            "phase2-groan": arcade.load_sound(SOUND_PATH + "enemy/enemy_oni_boss_groan.wav")
        },
        "player": {
            "attack": arcade.load_sound(SOUND_PATH + "player/player_attack_16bit.wav"),
            "damage": arcade.load_sound(SOUND_PATH + "player/player_damage.wav"),
            "jump": arcade.load_sound(SOUND_PATH + "player/player_jump_16bit.wav")
        },
        "powerups": {
            "attack-boost": arcade.load_sound(SOUND_PATH + "powerups/attack-boost.wav"),
            "heal": arcade.load_sound(SOUND_PATH + "powerups/heal.wav"),
            "jump-boost": arcade.load_sound(SOUND_PATH + "powerups/jump-boost.wav"),
            "speed-boost": arcade.load_sound(SOUND_PATH + "powerups/speed-boost.wav")
        },
        "user_interface": {
            "quit_button_press": arcade.load_sound(SOUND_PATH + "menu/button_press.wav"),
            "start_button_press": arcade.load_sound(SOUND_PATH + "menu/button_press2.wav")
        }
    }

    @staticmethod
    def play_sound(domain: str, sound_name: str, sound_volume=SOUND_VOLUME):
        sound = SoundManager.__sound_lists[domain][sound_name]
        player = arcade.play_sound(sound, sound_volume)
        # player object can be None if an error occurs (such as an unplayable sound)
        if player is None:
            print("Sound", domain + ":" + sound_name, "is not playable.")
            player = pyglet.media.Player()  # Avoids crash later on
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
            sound_player.sound.stop(sound_player.player)

    def __on_update(self):
        if SoundManager.__active_sounds is None:
            return
        # Remove sounds that have finished playing
        list_copy = SoundManager.__active_sounds
        for sound_player in list_copy:
            if sound_player.sound.get_stream_position(sound_player.player) == 0.0:
                SoundManager.__active_sounds.remove(sound_player)

    @staticmethod
    def start():
        # Updates used to monitor if played sounds have finished playing
        EventManager.add_listener("Update", SoundManager.__on_update)
