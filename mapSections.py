import random

import arcade

from collider import Collider
from entity import Entity
from enemyController import EnemyController
from spriteRenderer import SpriteRenderer
from transform import Transform
from powerUps import PowerUpHealth, PowerUpSpeed, PowerUpJump, PowerUpAttack



class SimpleBlock(Entity):
    def __init__(self, position):
        floor_sprite = arcade.Sprite("assets/tiles/ground_tile.png")
        floor_sprite_renderer = SpriteRenderer(floor_sprite)
        floor_transform = Transform(position, 0, 1.0)
        floor_collider = Collider(auto_generate_polygon="box")
        super(SimpleBlock, self).__init__("Block", ["Ground"], [floor_sprite_renderer, floor_transform, floor_collider],
                                          static=True)


class FoodStalls(Entity):
    def __init__(self, position):
        food_stall_sprite = arcade.Sprite("assets/tiles/food_stalls.png")
        food_stall_sprite_renderer = SpriteRenderer(food_stall_sprite)
        food_stall_transform = Transform(position, 0, 1.0)
        food_stall_collider = Collider(auto_generate_polygon="simple")
        super(FoodStalls, self).__init__("FoodStall", ["Ground"],
                                         [food_stall_sprite_renderer, food_stall_transform, food_stall_collider],
                                         static=True)


class GroundPit(Entity):
    def __init__(self, position):
        ground_pit_sprite = arcade.Sprite("assets/tiles/ground_pit_tile.png")
        ground_pit_sprite_renderer = SpriteRenderer(ground_pit_sprite)
        ground_pit_transform = Transform(position, 0, 1.0)
        super(GroundPit, self).__init__("GroundPit", [],
                                        [ground_pit_sprite_renderer, ground_pit_transform],
                                        static=True)


class Bench(Entity):
    def __init__(self, position):
        bench_sprite = arcade.Sprite("assets/tiles/bench.png")
        bench_sprite_renderer = SpriteRenderer(bench_sprite)
        bench_transform = Transform(position, 0, 1.0)
        bench_collider = Collider(auto_generate_polygon="simple")
        super(Bench, self).__init__("Bench", ["Ground"], [bench_sprite_renderer, bench_transform, bench_collider],
                                    static=True)


class Platform(Entity):
    def __init__(self, position):
        platform_sprite = arcade.Sprite("assets/tiles/wooden_platform.png")
        platform_sprite_renderer = SpriteRenderer(platform_sprite)
        platform_transform = Transform(position, 0, 1.0)
        platform_collider = Collider(auto_generate_polygon="simple")
        super(Platform, self).__init__("Platform", ["Ground", "Platform"],
                                       [platform_sprite_renderer, platform_transform, platform_collider], static=True)


class Enemy(Entity):
    def __init__(self, position):
        # Setup enemy(Red Oni)

        # Create an arcade.Sprite for the enemy(Red Oni)
        enemy_sprite = arcade.Sprite("assets/sprites/enemy/oni_idle_1.png")
        # Create a sprite renderer component
        enemy_sprite_renderer = SpriteRenderer(enemy_sprite)
        # Create a transform component for the enemy
        enemy_transform = Transform(position, 0, 1.0)
        # Create enemy controller component
        enemy_controller = EnemyController()
        # Create a collider component for the enemy (Will autogenerate hitbox when entity is created)
        enemy_collider = Collider(auto_generate_polygon="box")
        # Create the enemy entity and add all the components to it
        super(Enemy, self).__init__("Enemy", ["Enemy"],
                                    [enemy_sprite_renderer, enemy_transform, enemy_controller, enemy_collider],
                                    static=False)


# Load a map section from a file created by the visual editor
# All entities from this section will have their position offset by the given amount,
# and will be tagged with the given tag
def load_from_file(path, offset=(0, 0), tag=...):
    entities = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            line = line.split(":")
            if line[0] == "ground_tile.png":
                entities.append(SimpleBlock((float(line[1]), float(line[2]))))
            elif line[0] == "food_stalls.png":
                entities.append(FoodStalls((float(line[1]), float(line[2]))))
            elif line[0] == "ground_pit_tile.png":
                entities.append(GroundPit((float(line[1]), float(line[2]))))
            elif line[0] == "bench.png":
                entities.append(Bench((float(line[1]), float(line[2]))))
            elif line[0] == "wooden_platform.png":
                entities.append(Platform((float(line[1]), float(line[2]))))
            elif line[0] == "oni_idle_1.png":
                entities.append(Enemy((float(line[1]), float(line[2]))))
            elif line[0] == "cottoncandy.png":
                entities.append(PowerUpHealth((float(line[1]), float(line[2]))))
            elif line[0] == "onigiri.png":
                entities.append(PowerUpSpeed((float(line[1]), float(line[2]))))
            elif line[0] == "squid.png":
                entities.append(PowerUpJump((float(line[1]), float(line[2]))))
            elif line[0] == "dango.png":
                entities.append(PowerUpAttack((float(line[1]), float(line[2]))))
            entities[-1].transform.scale = float(line[3])  # Apply scale
    for entity in entities:
        if offset != (0, 0):
            entity.transform.position = (entity.transform.position[0] + offset[0], entity.transform.position[1] + offset[1])

        if tag is not None:
            entity.tags.append(tag)
        elif tag is ...:
            entity.tags.append(path)
        # Only omit adding tags if the function was explicitly passed None
    return entities


def tutorial():  # this is the section which will contain the tutorial sign
    entities = []
    tutorial_sprite = arcade.Sprite("assets/tiles/tutorial.PNG", 0.5)
    tutorial_sprite_renderer = SpriteRenderer(tutorial_sprite)
    tutorial_transform = Transform((0, 275))
    tutorial_collider = Collider(auto_generate_polygon="box")
    tutorial_entity = Entity("Tutorial Block", ["Tutorial"],
                             [tutorial_sprite_renderer, tutorial_transform, tutorial_collider], static=True)
    entities.append(tutorial_entity)
    for i in range(5):
        entities.append(SimpleBlock(((1 * i * 187), 93)))
    return entities


def section1():
    entities = []
    for i in range(10):
        entities.append(SimpleBlock(((1 * i * 187), 93)))

    entities.append(FoodStalls((1500, 500, 0)))
    return entities


def section2():
    entities = []
    # Set stalls to be behind the floor (So that they dont clip over the floor)
    entities.append(FoodStalls((1500, 407, 0)))
    # Create floor
    tutorial_sprite = arcade.Sprite("assets/tiles/tutorial_board.png")
    tutorial_sprite_renderer = SpriteRenderer(tutorial_sprite)
    tutorial_transform = Transform((80, 415))
    tutorial_collider = Collider(auto_generate_polygon="box")
    tutorial_entity = Entity("Tutorial Block", ["Tutorial"],
                             [tutorial_sprite_renderer, tutorial_transform, tutorial_collider], static=True)
    entities.append(tutorial_entity)
    for i in range(50):
        entities.append(SimpleBlock(((1 * i * 187), 93)))
    # Enemies at the base floor (before the stalls)
    for i in range(3):
        entities.append(Enemy((300 + (i * 300), 266, 0)))
    # Enemies on top of the tents
    for i in range(2):
        entities.append(Enemy((1300 + (i * 500), 714, 0)))
    return entities

def section3(): #section for working on enemy movement
    entities = []
    # Set stalls to be behind the floor (So that they dont clip over the floor)
    # Create floor
    tutorial_sprite = arcade.Sprite("assets/tiles/tutorial_board.png")
    tutorial_sprite_renderer = SpriteRenderer(tutorial_sprite)
    tutorial_transform = Transform((80, 415))
    tutorial_collider = Collider(auto_generate_polygon="box")
    tutorial_entity = Entity("Tutorial Block", ["Tutorial"],
                             [tutorial_sprite_renderer, tutorial_transform, tutorial_collider], static=True)
    entities.append(tutorial_entity)
    for i in range(50):
        entities.append(SimpleBlock(((1 * i * 187), 93)))
    # #Enemies at the base floor
    # for i in range(3):
    #     entities.append(Enemy((300 + (i * 300), 266, 0)))
    #
    # entities.append(PowerUpHealth((300, 300)))
    entities.append(PowerUpSpeed((700, 300)))

    return entities