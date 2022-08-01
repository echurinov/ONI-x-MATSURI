import random
from copy import deepcopy

from component import Component
from eventManager import EventManager
import mapSections
from gameManager import GameManager


class LevelSectionLoader(Component):
    def __init__(self):
        super(LevelSectionLoader, self).__init__("LevelSectionLoader")
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)

        # Current and previous section, use to know which sections to unload
        self.previous_section = None
        self.current_section = None

        # How far the player has progressed through the level
        # Marks the end of the previous_section
        self.current_offset = 0

        # List of all level files
        self.level_section_files = ["level1.dat", "level2.dat", "level3.dat"]
        # List of all the loaded level sections
        self.level_sections = []
        for level_file in self.level_section_files:
            # Add a tuple of (filename, length, entities) to the list
            length, entities = mapSections.load_from_file(level_file)
            self.level_sections.append((level_file, length, entities))
            print("Loaded level", level_file)

    # Helper to translate a level section by an offset
    def __tranform_section(self, section, offset):
        for entity in section:
            entity.transform.move(offset)

    def on_created(self):
        if self.current_section is None:
            print("Loading first section")
            # Load a copy of the first section
            section = deepcopy(random.choice(self.level_sections))
            # Add the section to the scene
            for entity in section[2]:
                GameManager.add_entity(entity)
            # Set current_section
            self.current_section = section


    def on_physics_update(self, dt):
        # Check player position, if they're more than halfway through a section, load the next section.
        # Also unload the section behind them
        # Sections are chosen randomly from the level_sections list


        player_position = self.parent.transform.position
        # Check if the player is more than halfway through the current section
        if player_position[0] > self.current_offset + (self.current_section[1] / 2):
            # Load a copy of the next section
            section = deepcopy(random.choice(self.level_sections))
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


