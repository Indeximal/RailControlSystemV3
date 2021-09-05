from typing import List, Optional

from .joint import RailJoint


class RailBlock:
	def __init__(self, a_joint: RailJoint, b_joint: RailJoint):
		self.a_joint: RailJoint = a_joint
		self.b_joint: RailJoint = b_joint
		self.a_connections: List(RailBlock) = list()
		self.b_connections: List(RailBlock) = list()
		