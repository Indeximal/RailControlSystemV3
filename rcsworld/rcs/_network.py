import random
from typing import Set, Callable, Any, Iterable

from .blocks import RailBlock, TransitRailBlock, CrossingRailBlock, \
    EndRailBlock, SwitchRailBlock


class RailNetwork:
    def __init__(self):
        self.blocks: Set[RailBlock] = set()

    def add_block(self, block: RailBlock):
        self.blocks.add(block)

    def add_blocks(self, blocks: Iterable[RailBlock]):
        self.blocks.update(blocks)

    @staticmethod
    def link(first_linker: Callable[[RailBlock], Any],
             second_linker: Callable[[RailBlock], Any]):
        """This function takes two bound linker methods and links the blocks"""
        first_block: RailBlock = first_linker.__self__
        second_block: RailBlock = second_linker.__self__
        first_linker(second_block)
        second_linker(first_block)

    def link_with_transit(self, first_linker: Callable[[RailBlock], Any],
             second_linker: Callable[[RailBlock], Any]) -> TransitRailBlock:
        """This function takes two bound linker methods and links the blocks
           with a transit block in between.
        """
        first_block: RailBlock = first_linker.__self__
        second_block: RailBlock = second_linker.__self__
        new_center = ((first_block.center[0] + second_block.center[0]) / 2,
                      (first_block.center[1] + second_block.center[1]) / 2)
        transit_block = TransitRailBlock(new_center)
        self.add_block(transit_block)
        self.link(first_linker, transit_block.set_a_link)
        self.link(second_linker, transit_block.set_b_link)
        return transit_block

    # def cross_transit_blocks(self):
    #     pass


def random_railyard(width, height, margin):
    """This function can generate a network that looks like a railyard"""
    network = RailNetwork()
    Y_Lanes = list(range(2 * margin, height - 2 * margin, 50))
    end_nodes_left = [EndRailBlock((margin, y)) for y in Y_Lanes]
    end_nodes_right = [EndRailBlock((width - margin, y)) for y in Y_Lanes]
    network.add_blocks(end_nodes_right)
    network.add_blocks(end_nodes_left)

    X = list(range(margin + 50, width - margin, 50))
    print()
    SWITCHES = [random.randint(1, len(Y_Lanes) - 1) for _ in X]
    S_DIR = [random.choice([1, -1]) for _ in X]
    switches_bottom = [SwitchRailBlock(
        (X[i], Y_Lanes[SWITCHES[i]])) for i in range(len(X))]
    switches_top = [SwitchRailBlock((X[i] + S_DIR[i] * 20,
                                     Y_Lanes[SWITCHES[i] - 1]))
                    for i in range(len(X))]

    network.add_blocks(switches_bottom)
    network.add_blocks(switches_top)

    # Connect the switches with each other
    for switch_top, switch_bottom in zip(switches_top, switches_bottom):
        network.link(switch_top.add_b_link, switch_bottom.add_b_link)

    # Connect the lanes
    for lane in range(len(Y_Lanes)):
        last_link = end_nodes_left[lane].set_a_link
        for i in range(len(X)):
            if SWITCHES[i] == lane + 1:
                if S_DIR[i] == -1:
                    network.link_with_transit(last_link, switches_top[i].set_a_link)
                    last_link = switches_top[i].add_b_link
                elif S_DIR[i] == 1:
                    network.link_with_transit(last_link, switches_top[i].add_b_link)
                    last_link = switches_top[i].set_a_link
            if SWITCHES[i] == lane:
                if S_DIR[i] == 1:
                    network.link_with_transit(last_link, switches_bottom[i].set_a_link)
                    last_link = switches_bottom[i].add_b_link
                elif S_DIR[i] == -1:
                    network.link_with_transit(last_link, switches_bottom[i].add_b_link)
                    last_link = switches_bottom[i].set_a_link
        network.link_with_transit(last_link, end_nodes_right[lane].set_a_link)

    return network