from __future__ import annotations

from typing import List, Optional
from abc import ABC, abstractmethod

from .types import Point


def remove_none_items(func):
    """This decorated removes all None occurrences in the return value"""
    def inner(*args, **kwargs):
        return [a for a in func(*args, **kwargs) if a]
    return inner


class RailBlock(ABC):
    """The base class for a single block of the rail network"""
    def __init__(self, center: Point):
        super().__init__()
        self.center = center

    @abstractmethod
    def next_blocks(self, from_block: Optional[RailBlock]) -> List[RailBlock]:
        pass


class TransitRailBlock(RailBlock):
    """A block with a A-side and a B-side link."""
    def __init__(self, center: Point):
        super().__init__(center)
        self._a_link: Optional[RailBlock] = None
        self._b_link: Optional[RailBlock] = None

    def set_a_link(self, link: RailBlock):
        self._a_link = link

    def set_b_link(self, link: RailBlock):
        self._b_link = link

    @remove_none_items
    def next_blocks(self, from_block: Optional[RailBlock]) -> List[RailBlock]:
        if not from_block:
            return [self._a_link, self._b_link]

        if from_block == self._a_link:
            return [self._b_link]
        elif from_block == self._b_link:
            return [self._a_link]
        else:
            return list()


class TransitStationRailBlock(TransitRailBlock):
    """A station block with a A-side and a B-side link."""
    def __init__(self, center: Point, name: str):
        super().__init__(center)
        self.name = name


class SwitchRailBlock(RailBlock):
    """A block with a single A-side link and many B-side links."""
    def __init__(self, center: Point):
        super().__init__(center)
        self._a_link: Optional[RailBlock] = None
        self._b_links: List[RailBlock] = list()

    def set_a_link(self, link: RailBlock):
        self._a_link = link

    def add_b_link(self, link: RailBlock):
        self._b_links.append(link)

    @remove_none_items
    def next_blocks(self, from_block: Optional[RailBlock]) -> List[RailBlock]:
        if not from_block:
            return [self._a_link] + list(self._b_links)

        if from_block == self._a_link:
            return self._b_links
        elif from_block in self._b_links:
            return [self._a_link]
        else:
            return list()


class CrossingRailBlock(RailBlock):
    """A block with many crossings with an A-side and B-side each"""
    def __init__(self, center: Point):
        super().__init__(center)
        self._a_links: List[RailBlock] = list()
        self._b_links: List[RailBlock] = list()

    def add_a_link(self, link: RailBlock):
        """Adds a link to the crossing, the connecting link is the next b-link
           to be added"""
        if len(self._a_links) > len(self._b_links):
            raise RuntimeError("The previous crossing has not been completed!")
        self._a_links.append(link)

    def add_b_link(self, link: RailBlock):
        if len(self._b_links) > len(self._a_links):
            raise RuntimeError("The previous crossing has not been completed!")
        self._b_links.append(link)

    def next_blocks(self, from_block: RailBlock) -> List[RailBlock]:
        for a_link, b_link in zip(self._a_links, self._b_links):
            if from_block == a_link:
                return [b_link]
            if from_block == b_link:
                return [a_link]
        return list()


class EndRailBlock(RailBlock):
    """A block with a single A-side link, but no B-side links."""
    def __init__(self, center: Point):
        super().__init__(center)
        self._a_link: Optional[RailBlock] = None

    def set_a_link(self, link: RailBlock):
        self._a_link = link

    @remove_none_items
    def next_blocks(self, from_block: Optional[RailBlock]) -> List[RailBlock]:
        if not from_block:
            return [self._a_link]
        return list()

