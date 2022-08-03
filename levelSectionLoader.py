import random
import copy

import arcade

from backgroundResizer import BackgroundResizer
from component import Component
from entity import Entity
from eventManager import EventManager
import mapSections
from gameManager import GameManager
from spriteRenderer import SpriteRenderer
from transform import Transform


class LevelSectionLoader(Component):
    def __init__(self):
        super(LevelSectionLoader, self).__init__("LevelSectionLoader")
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)

        # Current and previous section, use to know which sections to unload
        self.previous_section = None
        self.current_section = None

        # Create entity for background (will be copied and tiled)
        background_sprite = arcade.Sprite("assets/backgrounds/oni_background.png", 1.0)
        background_sprite_renderer = SpriteRenderer(background_sprite)
        background_transform = Transform((background_sprite.width, background_sprite.height / 2), 0, 1.0)
        self.background_resizer = BackgroundResizer()
        self.background_entity = Entity("Background", ["BackgroundTag"],
                                   [background_sprite_renderer, background_transform, self.background_resizer])


        # How far the player has progressed through the level
        # Marks the end of the previous_section
        self.current_offset = 0

        self.sections_gone_through = 0
        self.sections_before_tower = 8
        self.tower_teleport_x = None

        self.number_background_sections = 0

        self.tutorial_section_file = "tutorial.dat"
        self.tutorial_section = None

        self.tower_section_file = "tower.dat"
        self.tower_section = None
        # List of all level files
        self.level_section_files = ["level1.dat", "level2.dat", "level3.dat"]
        # List of all the loaded level sections
        self.level_sections = []
        for level_file in self.level_section_files:
            # Add a tuple of (filename, length, entities) to the list
            length, entities = mapSections.load_from_file(level_file)
            self.level_sections.append((level_file, length, entities))
            print("Loaded level", level_file)

        length, entities = mapSections.load_from_file(self.tutorial_section_file)
        self.tutorial_section = (self.tutorial_section_file, length, entities)
        print("Loaded tutorial level", self.tutorial_section_file)

        length, entities = mapSections.load_from_file(self.tower_section_file)
        self.tower_section = (self.tower_section_file, length, entities)
        print("Loaded tower level", self.tower_section_file)

        self.in_boss_level = False  # Don't do anything if we're in the boss level

    # Helper to translate a level section by an offset
    def __tranform_section(self, section, offset):
        for entity in section:
            entity.transform.move(offset)

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)

    def on_created(self):
        if self.in_boss_level:
            return
        # Don't do anything if the player isn't in the level yet
        # This function is called both when the player entity is created and when it is added to the scene
        if not self.parent.in_scene:
            return
        if self.current_section is None:
            print("Generating tutorial section")
            # Load a copy of the first section
            section = copy.deepcopy(self.tutorial_section)
            # Add the section to the scene
            for entity in section[2]:
                GameManager.add_entity(entity)
            # Set current_section
            self.current_section = section

    def on_physics_update(self, dt):
        if self.in_boss_level:
            return
        if self.tower_teleport_x is not None:  # Don't keep loading if we've loaded the tower
            return
        # Check player position, if they're more than halfway through a section, load the next section.
        # Also unload the section behind them
        # Sections are chosen randomly from the level_sections list

        # Don't do anything if the player isn't in the level yet
        if not self.parent.in_scene:
            return

        n_backgrounds = (self.parent.transform.position[0] + self.background_resizer.get_width()) // self.background_resizer.get_width()  # How many background sections we're through
        if n_backgrounds >= self.number_background_sections:
            background_copy = copy.deepcopy(self.background_entity)
            background_copy.transform.position = background_copy.transform.position[0] * self.number_background_sections, background_copy.transform.position[1]
            GameManager.add_background_entity(background_copy)
            self.number_background_sections += 1

        player_position = self.parent.transform.position
        # Check if the player is more than halfway through the current section
        if player_position[0] > self.current_offset + (self.current_section[1] / 2):
            self.sections_gone_through += 1
            if self.sections_gone_through > self.sections_before_tower:
                # load tower section
                print("Loading tower section")
                section = copy.deepcopy(self.tower_section)
                self.tower_teleport_x = self.current_offset + section[1]
            else:
                # Load a copy of the next section
                section = copy.deepcopy(random.choice(self.level_sections))
            # Translate that section to put it after the end of the current loaded section
            self.__tranform_section(section[2], (self.current_offset + self.current_section[1], 0))
            # Add the section to the scene
            for entity in section[2]:
                GameManager.add_entity(entity)
            # Unload the previous section
            if self.previous_section is not None:
                for entity in self.previous_section[2]:
                    # Do it this way instead of using tags, as that won't work if the same section is repeated
                    GameManager.remove_entity(entity)
                print("Unloaded previous section", self.previous_section[0])
                del self.previous_section  # not sure if this is needed, might help with memory issues

            # Update previous_section to point to the old current section
            self.previous_section = self.current_section

            # Update the current section to the new section
            self.current_section = section
            # Update the offset
            # Use previous_section[1] instead of current_section[1] so that the offset points to the right place
            self.current_offset += self.previous_section[1]

            print("Loaded new section", self.current_section[0])

    def get_final_coord(self):
        return self.current_offset
