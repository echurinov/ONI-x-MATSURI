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
        super(SimpleBlock, self).__init__("Block", ["Ground"], [floor_sprite_renderer, floor_transform, floor_collider])

def tutorial(): #this is the section which will contain the tutorial sign
    entities = []
    tutorial_sprite = arcade.Sprite("assets/tiles/tutorial.PNG", 0.5)
    tutorial_sprite_renderer = SpriteRenderer(tutorial_sprite)
    tutorial_transform = Transform((0, 275))
    tutorial_collider = Collider(auto_generate_polygon="box")
    tutorial_entity = Entity("Tutorial Block", ["Tutorial"], [tutorial_sprite_renderer, tutorial_transform, tutorial_collider])
    entities.append(tutorial_entity)
    for i in range(10):
        entities.append(SimpleBlock(((1 * i * 187), 93)))
    return entities

def section1():
    entities = []
    for i in range(10):
        entities.append(SimpleBlock(((1 * i * 187), 93)))
    return entities