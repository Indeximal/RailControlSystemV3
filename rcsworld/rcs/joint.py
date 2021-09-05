import math


class RailJoint:
	def __init__(self, x: float, y: float, angle: float):
		self.x = x
		self.y = y
		if abs(angle) > math.pi / 2:
			raise ValueError("angle is not in range -pi/2 to pi/2")
			
		self.angle = angle
