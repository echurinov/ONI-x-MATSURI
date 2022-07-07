import arcade

from component import Component
from eventManager import EventManager


class EnemyController(Component):

    # Called every time physics get updated (currently every frame)
    # Deals with all enemy movement and collision
    def on_physics_update(self, dt):
        # Round velocity to 0 if we're close enough
        epsilon = 0.001
        if abs(self.__velocity[0]) < epsilon:
            self.__velocity = (2, self.__velocity[1])
        if abs(self.__velocity[1]) < epsilon:
            self.__velocity = (self.__velocity[0], 0)

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):
        # Animation states
        if self.__velocity[0] < 0: #(and not self.__position_x < x_left_boundary
            self.__animation_state = "walk_L"
        elif self.__velocity[0] > 0: #(and not self.__position_x > x_right_boundary
            self.__animation_state = "walk_R"
        else:
            self.__animation_state = "idle"

        # Animation
        self.__animation_timer += 1
        if self.__animation_timer > self.__animation_data[self.__animation_state]["frame_delay"]:
            # Reset timer
            self.__animation_timer = 0
            # Increment counter
            self.__animation_frame = (self.__animation_frame + 1) % self.__animation_data[self.__animation_state]["num_frames"]
            # Switch sprite
            self.__sprite_renderer.switch_sprite(self.__animation_data[self.__animation_state]["frames"][self.__animation_frame])

    def __init__(self):
        super().__init__("EnemyController")

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        # Private variables for enemy health
        self.__health = 6
        self.__taking_damage = False

        # Sprite switching (animation)
        self.__animation_timer = 0  # Frames since last change
        self.__animation_frame = 0  # Which frame we're in
        self.__animation_state = "idle"
        # Dictionary for frames for animations

        self.__animation_data = {
            "idle": {
                "name_prefix": "oni_idle_",
                "num_frames": 2,
                "frame_delay": 30,
                "frames": []
            },
            "walk_L": {
                "name_prefix": "oni_walk_L_",
                "num_frames": 4,
                "frame_delay": 5,
                "frames": []
            },
            "walk_R": {
                "name_prefix": "oni_walk_R_",
                "num_frames": 4,
                "frame_delay": 5,
                "frames": []
            }
        }
        for animation_name, animation in self.__animation_data.items():
            for i in range(animation["num_frames"]):
                animation["frames"].append(arcade.Sprite("assets/sprites/enemy/" + animation["name_prefix"] + str(i+1) +".png", 0.5))

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")

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
