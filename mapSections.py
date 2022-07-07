import random

import arcade

from collider import Collider
from entity import Entity
from gameManager import GameManager
from eventManager import EventManager
from physicsObject import PhysicsObject
from playerController import PlayerController
from spriteRenderer import SpriteRenderer
from transform import Transform

class SimpleBlock(Entity):
    def __init__(self, position):
        floor_sprite = arcade.Sprite("assets/tiles/ground_tile.png")
        floor_sprite_renderer = SpriteRenderer(floor_sprite)
        floor_transform = Transform(position, 0, (0.25, 0.25))
        floor_collider = Collider(auto_generate_polygon="box")
        super(SimpleBlock, self).__init__("Block", ["Ground"], [floor_sprite_renderer, floor_transform, floor_collider], static=True)

class FoodStalls(Entity):
    def __init__(self, position):
        food_stall_sprite = arcade.Sprite("assets/tiles/food_stalls.png")
        food_stall_sprite_renderer = SpriteRenderer(food_stall_sprite)
        food_stall_transform = Transform(position, 0, (0.25, 0.25))
        food_stall_collider = Collider(auto_generate_polygon="box")
        super(FoodStalls, self).__init__("FoodStall", ["Ground"], [food_stall_sprite_renderer, food_stall_transform, food_stall_collider], static=True)

class GroundPit(Entity):
    def __init__(self, position):
        ground_pit_sprite = arcade.Sprite("assets/tiles/ground_pit_tile.png")
        ground_pit_sprite_renderer = SpriteRenderer(ground_pit_sprite)
        ground_pit_transform = Transform(position, 0, (0.25, 0.25))
        ground_pit_collider = Collider(auto_generate_polygon="box")
        super(GroundPit, self).__init__("Block", ["Ground"], [ground_pit_sprite_renderer, ground_pit_transform, ground_pit_collider], static=True)

class Bench(Entity):
    def __init__(self, position):
        bench_sprite = arcade.Sprite("assets/tiles/bench.png")
        bench_sprite_renderer = SpriteRenderer(bench_sprite)
        bench_transform = Transform(position, 0, (0.25, 0.25))
        bench_collider = Collider(auto_generate_polygon="box")
        super(Bench, self).__init__("Block", ["Ground"], [bench_sprite_renderer, bench_transform, bench_collider], static=True)

class Platform(Entity):
    def __init__(self, position):
        platform_sprite = arcade.Sprite("assets/tiles/wooden_platform.png")
        platform_sprite_renderer = SpriteRenderer(platform_sprite)
        platform_transform = Transform(position, 0, (0.25, 0.25))
        platform_collider = Collider(auto_generate_polygon="box")
        super(Platform, self).__init__("Block", ["Ground"], [platform_sprite_renderer, platform_transform, platform_collider], static=True)

def tutorial(): #this is the section which will contain the tutorial sign
    entities = []
    tutorial_sprite = arcade.Sprite("assets/tiles/tutorial.PNG", 0.5)
    tutorial_sprite_renderer = SpriteRenderer(tutorial_sprite)
    tutorial_transform = Transform((0, 275))
    tutorial_collider = Collider(auto_generate_polygon="box")
    tutorial_entity = Entity("Tutorial Block", ["Tutorial"], [tutorial_sprite_renderer, tutorial_transform, tutorial_collider], static=True)
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

