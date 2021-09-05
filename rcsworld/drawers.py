import pygame
import numpy as np

from .rcs.blocks import SwitchRailBlock, TransitRailBlock, EndRailBlock
from .rcs.network import RailNetwork


LINK_LENGTH = 20
NODE_RADIUS = 4
FREE_COLOR = (255, 255, 255)
A_COLOR = (255, 255, 0)
B_COLOR = (0, 255, 255)


_drawer_directory = {}


def draw_thing(screen, thing):
    drawer = _drawer_directory.get(type(thing))
    if drawer:
        drawer(screen, thing)
    else:
        raise NotImplementedError("The drawer for " + str(thing) + "doesn't "
                                                                   "exist")


def register_drawer(for_class):
    def decorator(function):
        _drawer_directory[for_class] = function
        return function
    return decorator


@register_drawer(RailNetwork)
def draw_rail_network(screen, network: RailNetwork):
    for block in network.blocks:
        draw_thing(screen, block)


@register_drawer(TransitRailBlock)
def draw_transit_block(screen, block: TransitRailBlock):
    pygame.draw.line(screen, FREE_COLOR, block._a_link.center,
                     block._b_link.center)


def draw_link(screen, color, center, destination):
    pos = np.array(center)
    dest = np.array(destination)
    diff = dest - pos
    length = np.linalg.norm(diff)
    endpoint = diff / length * LINK_LENGTH + pos
    pygame.draw.line(screen, color, center, endpoint, 3)


@register_drawer(SwitchRailBlock)
def draw_switch_block(screen, block: SwitchRailBlock):
    pygame.draw.circle(screen, FREE_COLOR, block.center, NODE_RADIUS)
    if block._a_link:
        draw_link(screen, A_COLOR, block.center, block._a_link.center)
    for link in block._b_links:
        draw_link(screen, B_COLOR, block.center, link.center)

@register_drawer(EndRailBlock)
def draw_switch_block(screen, block: EndRailBlock):
    start_point = np.array(block.center) + np.array([0, LINK_LENGTH / 2])
    end_point = np.array(block.center) + np.array([0, - LINK_LENGTH / 2])
    pygame.draw.line(screen, FREE_COLOR, start_point, end_point)
