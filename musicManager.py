"""Background music implementation taken from https://api.arcade.academy/en/2.5.7/examples/background_music.html"""

import arcade
import time

from eventManager import EventManager

MUSIC_VOLUME = 0.7
MUSIC_PATH = "assets/sounds/music/"

# Handles all loading and playing of music for all views in the game (Main Menu, Game View, Lose Screen, Win Screen, etc)
# Everything in this class is static


class MusicManager:
    __music_lists = {
        "boss_view": [],
        "game_view": [],
        "lose_view": [],
        "start_view": [],
        "win_view": []
    }
    __current_list = None
    __current_song_index = 0
    __current_player = None
    __current_song = None
    __loop = True

    @staticmethod
    def advance_song():
        """ Advance our pointer to the next song. This does NOT start the song. """
        MusicManager.__current_song_index += 1
        if MusicManager.__current_song_index >= len(MusicManager.__current_list) and MusicManager.__loop:
            MusicManager.__current_song_index = 0
        print(f"Advancing song to {MusicManager.__current_song_index}.")

    @staticmethod
    def play_song():
        """ Play the song. """
        # Stop what is currently playing.
        MusicManager.stop_song()

        # Play the next song
        MusicManager.set_song()
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    @staticmethod
    def stop_song():
        if MusicManager.__current_song:
            MusicManager.__current_song.stop(MusicManager.__current_player)

    @staticmethod
    def set_song():
        if len(MusicManager.__current_list) == 0:
            print("Couldn't change list! No songs in this list!")
            return
        MusicManager.stop_song()
        print(f"Playing {MusicManager.__current_list[MusicManager.__current_song_index]}")
        MusicManager.__current_song = arcade.Sound(MusicManager.__current_list[MusicManager.__current_song_index], streaming=True)
        MusicManager.__current_player = MusicManager.__current_song.play(MUSIC_VOLUME)

    @staticmethod
    def change_list(list_name: str, loop=True):
        MusicManager.__loop = loop
        MusicManager.stop_song()
        MusicManager.__current_list = MusicManager.__music_lists[list_name]
        MusicManager.__current_song_index = 0
        MusicManager.set_song()

    def __on_update(self):
        if MusicManager.__current_list is None:
            print("No music list has been selected.")
            return
        elif len(MusicManager.__current_list) == 0:
            print("Current music list has no songs!")
            return
        song_pos = MusicManager.__current_song.get_stream_position(MusicManager.__current_player)
        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if song_pos == 0.0:
            MusicManager.advance_song()
            MusicManager.play_song()

    @staticmethod
    def start():
        MusicManager.__music_lists["boss_view"] = [MUSIC_PATH + "boss_stage_music.mp3"]
        MusicManager.__music_lists["game_view"] = [MUSIC_PATH + "main_stage_music.mp3"]
        MusicManager.__music_lists["lose_view"] = [MUSIC_PATH + "J 3ds3 24 Btl Lose 3ds.mp3"]
        MusicManager.__music_lists["start_view"] = [MUSIC_PATH + "main_menu_music.mp3"]
        MusicManager.__music_lists["win_view"] = []

        EventManager.add_listener("Update", MusicManager.__on_update)
