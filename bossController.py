import arcade

from component import Component
from eventManager import EventManager
from gameManager import GameManager
from soundManager import SoundManager
from powerUps import PowerUpJump, PowerUpSpeed, PowerUpAttack, PowerUpHealth
import random
import math

IDLE_TIMER = 5
DAMAGE_TIMER = 5
PREPARE_ATTACK_TIMER = 2
ATTACK_TIME = 2 # How long the boss attacks
ATTACK_TIMER = 7 # How long before the boss can attack again
MOVING_SPEED = 1
SHAKE_TIMER = 0.7 # How long between camera shakes
HEALTH = 10
PHASE_2_HEALTH = 9
PHASE_3_HEALTH = 2
ANGRY_TIMER = 3


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
        # Cheeky little opening animation (boss drops down, player cannot move)
        if self.__start_animation:
            self.__moving = False
            self.__idle = True
            self.__idle_timer = IDLE_TIMER + 4
            if self.__transform.position[1] > 1396:
                self.__transform.position = (self.__transform.position[0], self.__transform.position[1] - 7)
                #print(self.__transform.position)
            else:
                self.__transform.position = (self.__transform.position[0], self.__transform.position[1] - 3)
                SoundManager.play_sound("enemy_oni_boss", "drop")
                self.camera_shake(10)
                self.__start_animation = False

        # Don't animate if it isn't active yet
        if not self.parent.in_scene:
            return
        if self.__damage_timer > 0:
            self.__sprite_renderer.sprite.color = (255, 100 - self.__red_amount, 100 - self.__red_amount)
        else:
            self.__sprite_renderer.sprite.color = (255, 255 - self.__red_amount, 255 - self.__red_amount)

        chance = random.randint(0, 100)

        # Boss phase 1: boss moves back and forth across the screen, attacks sometimes
        if self.__phase == 0:
            # If boss has been idle for more than IDLE_TIMER
            if self.__idle and self.__idle_timer < 0:
                # Give a chance that the boss will move
                if chance % 10 == 0:
                    self.__moving = True
                    self.__idle = False

            # Give chance that boss will prepare to attack
            if chance % self.__attack_chance == 0 and not self.__prepare_attack and not self.__is_attacking and self.__attack_timer < 0:
                self.__moving = False
                self.__idle = False
                self.__default = False
                self.__prepare_attack = True
                self.__is_attacking = False
                self.__prepare_attack_timer = PREPARE_ATTACK_TIMER

            if self.__prepare_attack_timer < 0 and self.__prepare_attack:
                self.__moving = True
                self.__is_attacking = True
                self.__attack_time = ATTACK_TIME
                self.__prepare_attack = False
                self.__default = False
                self.__idle = False

            if self.__is_attacking:
                self.camera_shake(3)


            if self.__is_attacking and self.__attack_time < 0:
                self.__is_attacking = False
                self.__default = True
                self.__attack_timer = ATTACK_TIMER

            # If the boss is moving to the other side
            if self.__moving and not self.__idle:
                if self.__right_side: # If the boss started on the right side
                    if self.__transform.position[0] >= self.__left_side_position:
                        self.__transform.position = (self.__transform.position[0] - MOVING_SPEED, self.__transform.position[1])
                    else:
                        self.__moving = False
                        self.__idle = True
                        self.__idle_timer = IDLE_TIMER
                        self.__right_side = False

                else:
                    if self.__transform.position[0] <= self.__right_side_position:
                        self.__transform.position = (self.__transform.position[0] + MOVING_SPEED, self.__transform.position[1])
                    else:
                        self.__moving = False
                        self.__idle = True
                        self.__idle_timer = IDLE_TIMER
                        self.__right_side = True

        if self.__health < PHASE_2_HEALTH and self.__phase == 0:
            self.camera_shake(10)
            self.power_up_drop(5)
            self.__phase = 1
            self.__is_attacking = True
            self.__idle = False
            self.__default = False
            self.__moving = False
            self.__prepare_attack = False
            self.__attack_timer = 3
            self.__angry_timer = ANGRY_TIMER

        if self.__angry_timer > 0:
            self.__red_amount + 10
            if self.__red_amount > 255:
                self.__red_amount = 255
            self.__sprite_renderer.sprite.color = (255, 255 - self.__red_amount, 255 - self.__red_amount)


        # Boss phase 2: Boss moves back and forth across the screen, continously attacking
        if self.__phase == 1:
            # go idle for a second
            pass

        # Animation update
        self.update_animation()

        # Have all power-ups fall
        for power_up in self.__power_up_list:
            if power_up.transform.position[1] > 1325:
                power_up.transform.move((0, -10))

    def on_physics_update(self, dt):
        self.__idle_timer -= dt
        self.__prepare_attack_timer -= dt
        self.__attack_time -= dt
        self.__damage_timer -= dt
        self.__attack_timer -= dt
        self.__shake_timer -= dt
        self.__angry_timer -= dt
        return

    def __init__(self):
        super().__init__("BossController")

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        self.__attacking_sprite_1 = arcade.Sprite("assets/sprites/enemy/boss_attack_1.png")
        self.__attacking_sprite_2 = arcade.Sprite("assets/sprites/enemy/boss_attack_2.png")

        # Timers for enemy moving
        self.__idle_timer = IDLE_TIMER

        # Private variables for enemy health
        self.__health = HEALTH
        self.__taking_damage = False
        self.__damage_timer = 0.0

        # Holds all the powerups currently on screen
        self.__power_up_list = []

        # Variables for enemy position
        self.__right_side = True
        self.__moving = False
        self.__idle = True
        self.__direction = 1  # Direction is 1 for right, -1 for left
        self.__left_side_position = 0
        self.__right_side_position = 0
        self.__move_speed = 10

        # Variables for attacking
        self.__attack_power = 1
        self.__attack_chance = 10
        self.__prepare_attack = False
        self.__is_attacking = False
        self.__attack_time = ATTACK_TIME
        self.__attack_timer = ATTACK_TIMER
        self.__prepare_attack_timer = PREPARE_ATTACK_TIMER
        self.__phase = 0

        # Animation
        self.current_texture = 0
        self.__default = True
        self.__squish_amount = 0
        self.__shake_timer = SHAKE_TIMER
        self.__start_animation = True
        self.__angry_timer = ANGRY_TIMER
        self.__red_amount = 0

        # Idle animations
        idle_1 = (arcade.load_texture("assets/sprites/enemy/boss_1.png"), arcade.load_texture("assets/sprites/enemy/boss_1.png"))
        self.idle_texture = idle_1

        prepare_attack_1 = (arcade.load_texture("assets/sprites/enemy/boss_2.png"), arcade.load_texture("assets/sprites/enemy/boss_2.png"))
        prepare_attack_2 = (arcade.load_texture("assets/sprites/enemy/boss_3.png"), arcade.load_texture("assets/sprites/enemy/boss_3.png"))
        self.prepare_attack_texture = (prepare_attack_1, prepare_attack_2)

        # Attack animation
        attack_1 = (arcade.load_texture("assets/sprites/enemy/boss_3.png"), arcade.load_texture("assets/sprites/enemy/boss_attack_1.png"))
        attack_2 = (arcade.load_texture("assets/sprites/enemy/boss_attack_2.png"), arcade.load_texture("assets/sprites/enemy/boss_attack_2.png"))
        attack_3 = (arcade.load_texture("assets/sprites/enemy/boss_attack_1.png"), arcade.load_texture("assets/sprites/enemy/boss_attack_1.png"))
        self.attack_texture = (attack_1, attack_2, attack_3)


    def on_remove(self):
        self.camera_shake(5)
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        EventManager.remove_listener("Update", self.on_update)

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        EventManager.add_listener("Update", self.on_update)
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)

    # Call to drop a bunch of power-ups on screen
    def power_up_drop(self, amount):
        power_up_list = ["PowerUpHealth", "PowerUpSpeed", "PowerUpJump", "PowerUpAttack"]
        to_spawn = []

        # randomly pick which powerups to spawn
        for i in range(amount):
            to_spawn.append(power_up_list[random.randint(0, 4) - 1])

        # determine the random positions for the powerups
        for power_up in to_spawn:
            temp = None
            position = random.randint(self.__left_side_position - 350, self.__right_side_position + 350)
            if power_up == "PowerUpHealth":
                temp = PowerUpHealth((position, 2500))
                GameManager.add_entity(temp)
            elif power_up == "PowerUpJump":
                temp = PowerUpJump((position, 2500))
                GameManager.add_entity(temp)
            elif power_up == "PowerUpAttack":
                temp = PowerUpAttack((position, 2500))
                GameManager.add_entity(temp)
            elif power_up == "PowerUpSpeed":
                temp = PowerUpSpeed((position, 2500))
                GameManager.add_entity(temp)
            self.__power_up_list.append(temp)
        return

    # I USED THE FOLLOWING LINK AS REFERENCE FOR THIS: https://api.arcade.academy/en/latest/examples/sprite_move_scrolling_shake.html
    def camera_shake(self, amount):
        if self.__shake_timer < 0:
            self.__shake_timer = SHAKE_TIMER
            shake_direction = -5
            # Calculate a vector based on that
            shake_vector = (
                math.cos(shake_direction) * amount,
                math.sin(shake_direction) * amount
            )
            # Frequency of the shake
            shake_speed = 1.5
            # How fast to damp the shake
            shake_damping = 0.9
            # Do the shake
            GameManager.main_camera.shake(shake_vector,
                                      speed=shake_speed,
                                      damping=shake_damping)



    # Adds squish to the movement to make boss look more lively
    def squish_amount(self, texture):
        curr_sprite = self.__sprite_renderer.sprite
        if not self.__moving:
            self.__squish_amount = 0
            #self.__sprite_renderer.set_texture(texture)
        else:
            self.__squish_amount += 1
            if self.__squish_amount == 4:
                self.__squish_amount = 0

        # Rachel: Somehow change squish amount of the texture here plz :D
        scale = 1 - self.__squish_amount / 20
        new_sprite = arcade.Sprite(scale=1.0, image_width=curr_sprite.width, image_height=curr_sprite.height - 2, center_x=curr_sprite.center_x, center_y=curr_sprite.center_y, texture=curr_sprite.texture)
        self.__sprite_renderer.switch_sprite(new_sprite)
        #print(str(scale) + " " + str(new_sprite.height))

    def update_animation(self):
        # If boss is not preparing to attack or attacking
        if self.__default:
            texture = self.idle_texture[0]
            self.squish_amount(texture)
            self.__collider.generate_hitbox_from_sprite()
            return

        # If the boss is preparing to attack
        if self.__prepare_attack:
            self.current_texture += 1
            if self.current_texture > (2 * 60) - 1:
                self.current_texture = 0
            frame = self.current_texture // 60
            texture = self.prepare_attack_texture[frame][0]
            self.squish_amount(texture)
            return

        # If the boss is attacking
        if self.__is_attacking:
            self.current_texture += 1
            if self.current_texture > (3 * 9) - 1:
                self.current_texture = 0
            frame = self.current_texture // 9
            texture = self.attack_texture[frame][0]
            self.squish_amount(texture)
            self.__collider.generate_hitbox_from_sprite()
            return
        return

    def set_left_side_position(self, position):
        self.__left_side_position = position

    def set_right_side_position(self, position):
        self.__right_side_position = position

    def get_attack_power(self):
        return self.__attack_power

    def set_collider(self, collider):
        self.__collider = collider

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
