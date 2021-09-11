from typing import List, Optional

from .point import DirectedPoint


class RailBlock:
	def __init__(self, a_point: DirectedPoint, b_point: DirectedPoint):
		self.a_point: DirectedPoint = a_point
		self.b_point: DirectedPoint = b_point
		self.a_connections: List(RailBlock) = list()
		self.b_connections: List(RailBlock) = list()
		