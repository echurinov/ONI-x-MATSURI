import arcade

from component import Component
from eventManager import EventManager
from gameManager import GameManager
from soundManager import SoundManager


class BossController(Component):
    def take_damage(self, amount):
        if self.__damage_timer > 0:
            return
        self.__damage_timer = 1.0
        self.__health = self.health - amount
        if self.__health < 0:
            SoundManager.play_sound("enemy_oni", "death")
            GameManager.remove_entity(self.parent)
        else:
            SoundManager.play_sound("enemy_oni", "death")
        self.__taking_damage = True

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):
        # Don't animate if it isn't active yet
        if not self.parent.in_scene:
            return
        if self.__damage_timer > 0:
            self.__sprite_renderer.sprite.color = (255, 100, 100)
        else:
            self.__sprite_renderer.sprite.color = (255, 255, 255)

        if self.__standing:
            self.__animation_state = "idle"

        if self.__walking and self.__direction == 1:  # Walking to the right
             self.__animation_state = "walk_L"

        if self.__walking and self.__direction == -1:  # Walking to the left
            self.__animation_state = "walk_R"

        # Animation
        self.__animation_timer += 1
        if self.__animation_timer > self.__animation_data[self.__animation_state]["frame_delay"]:
            # Reset timer
            self.__animation_timer = 0
            # Increment counter
            self.__animation_frame = (self.__animation_frame + 1) % self.__animation_data[self.__animation_state][
                "num_frames"]
            # Switch sprite
            self.__sprite_renderer.switch_sprite(
                self.__animation_data[self.__animation_state]["frames"][self.__animation_frame])

    def __init__(self):
        super().__init__("BossController")

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        # Timers for enemy walking
        self.__moving_timer = WALKING_TIMER
        self.__idle_timer = IDLE_TIMER

        # Private variables for enemy health
        self.__health = 1
        self.__taking_damage = False
        self.__damage_timer = 0.0

        # Sprite switching (animation)
        self.__animation_timer = 0  # Frames since last change
        self.__animation_frame = 0  # Which frame we're in
        self.__animation_state = "idle"

        self.__moving = False
        self.__standing = True
        self.__direction = 1  # Direction is 1 for right, -1 for left

        # Variables for attacking
        self.__prepare_attack = False
        self.__is_attacking = False

        # Dictionary for frames for animations

        self.__animation_data = {
            "idle": {
                "name_prefix": "boss_",
                "num_frames": 1,
                "frame_delay": 30,
                "frames": []
            },
            "prepare_attack": {
                "name_prefix": "boss_",
                "num_frames": 4,
                "frame_delay": 20,
                "frames": []
            },
            "attack": {
                "name_prefix": "boss_attack_",
                "num_frames": 2,
                "frame_delay": 10,
                "frames": []
            }
        }
        for animation_name, animation in self.__animation_data.items():
            for i in range(animation["num_frames"]):
                animation["frames"].append(
                    arcade.Sprite("assets/sprites/enemy/" + animation["name_prefix"] + str(i + 1) + ".png", 0.5))

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        EventManager.remove_listener("Update", self.on_update)

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        EventManager.add_listener("Update", self.on_update)
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)

    @property
    def touching_ground(self):
        return self.__touching_ground

    @property
    def velocity(self):
        return self.__velocity

    @property
    def health(self):
        return self.__health

    @property
    def taking_damage(self):
        return self.__taking_damage
