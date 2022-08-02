import arcade

from component import Component
from eventManager import EventManager
from gameManager import GameManager
from soundManager import SoundManager

IDLE_TIMER = 1
MOVING_TIMER = 3
DAMAGE_TIMER = 5
PREPARE_ATTACK_TIMER = 0.3
ATTACK_TIME = 0.3
ATTACK_TIMER = 3


class BossController(Component):
    def take_damage(self, amount):
        if self.__damage_timer > 0:
            return
        self.__damage_timer = 5
        self.__health = self.health - amount
        if self.__health < 0:
            SoundManager.play_sound("enemy_oni_boss", "death")
            GameManager.remove_entity(self.parent)
        else:
            SoundManager.play_sound("enemy_oni_boss", "damage")
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

        # Animation update
        self.update_animation()

    def on_physics_update(self, dt):
        self.__idle_timer -= dt
        self.__attack_timer -= dt
        self.__attack_time -= dt
        self.__damage_timer -= dt
        self.__moving_timer -= dt
        return

    def __init__(self):
        super().__init__("BossController")

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        # Timers for enemy moving
        self.__moving_timer = MOVING_TIMER
        self.__idle_timer = IDLE_TIMER
        self.__attack_time = ATTACK_TIME
        self.__attack_timer = PREPARE_ATTACK_TIMER

        # Private variables for enemy health
        self.__health = 1
        self.__taking_damage = False
        self.__damage_timer = 0.0

        self.__moving = False
        self.__standing = True
        self.__direction = 1  # Direction is 1 for right, -1 for left

        # Variables for attacking
        self.__prepare_attack = False
        self.__is_attacking = False

        # Animation
        self.current_texture = 0
        self.__default = True

        # Idle animations
        idle_1 = (arcade.load_texture("assets/sprites/enemy/boss_1.png"), arcade.load_texture("assets/sprites/enemy/boss_1.png"))
        self.idle_texture = (idle_1)

        prepare_attack_1 = (arcade.load_texture("assets/sprites/enemy/boss_2.png"), arcade.load_texture("assets/sprites/enemy/boss_2.png"))
        prepare_attack_2 = (arcade.load_texture("assets/sprites/enemy/boss_3.png"), arcade.load_texture("assets/sprites/enemy/boss_3.png"))
        self.prepare_attack_texture = (prepare_attack_1, prepare_attack_2)

        # Attack animation
        attack_1 = (arcade.load_texture("assets/sprites/enemy/boss_attack_1.png"), arcade.load_texture("assets/sprites/enemy/boss_attack_1.png"))
        attack_2 = (arcade.load_texture("assets/sprites/enemy/boss_attack_2.png"), arcade.load_texture("assets/sprites/enemy/boss_attack_2.png"))
        self.attack_texture = (attack_1, attack_2)


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

    def update_animation(self):
        # If boss is not preparing to attack or attacking
        if self.__default:
            self.__sprite_renderer.set_texture(self.idle_texture[0])
            return

        # If the boss is preparing to attack
        if self.__prepare_attack:
            self.current_texture += 1
            if self.current_texture > (2 * 9) - 1:
                self.current_texture = 0
            frame = self.current_texture // 9
            self.__sprite_renderer.set_texture(self.prepare_attack_texture[frame])
            return

        # If the boss is attacking
        if self.__is_attacking:
            self.__current_texture += 1
            if self.current_texture > (2 * 9) - 1:
                self.current_texture = 0
            frame = self.current_texture // 9
            self.__sprite_renderer.set_texture(self.attack_texture[frame])
            return
        return

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
