from typing import Tuple

import numpy as np


def lerp(a, b, t):
	return a*(1-t) + b*t


class DirectedPoint:
	def __init__(self, pos: Tuple[float], dir_tup: Tuple[float]):
		self.pos_vec = np.array(pos)
		self.dir_vec = np.array(dir_tup)
		
		if len(self.pos_vec) != 2:
			raise Exception("Position must be of dimension two")
		
		if len(self.dir_vec) != 2:
			raise Exception("Direction must be of dimension two")
	
	def opposite(self):
		return DirectedPoint(self.pos_vec, -self.dir_vec)	
	
	def bezier_to(self, other, t):
		control_self = self.pos_vec + self.dir_vec
		control_other = other.pos_vec + other.dir_vec
		
		# p1 = lerp(self.pos_vec, control_self, t)
		# p2 = lerp(control_self, control_other, t)
		# p3 = lerp(control_other, other.pos_vec, t)
		
		# p4 = lerp(p1, p2, t)
		# p5 = lerp(p2, p3, t)
		
		# p = lerp(p4, p5)
		
		t2 = t*t
		t3 = t2*t
		p = self.pos_vec * (-t3 + 3*t2 - 3*t + 1) \
			+ control_self * (3*t3 - 6*t2 + 3*t) \
			+ control_other * (-3*t3 + 3*t2) \
			+ other.pos_vec * t3
		
		d = self.pos_vec * (-3*t2 + 6*t - 3) \
			+ control_self * (9*t2 - 12*t + 3) \
			+ control_other * (-9*t2 + 6*t) \
			+ other.pos_vec * (3*t2)
			
		return DirectedPoint(p, d)

	def bezier_boudingbox_to(self, other):
		a = self.pos_vec
		b = self.pos_vec + self.dir_vec
		c = other.pos_vec + other.dir_vec
		d = other.pos_vec
		discriminants = -a*c + a*d + b**2 - b*c - b*d + c**2
		divisor	= (a - 3*b + 3*c - d)
		
		x = [self.pos_vec[0], other.pos_vec[0]]
		if discriminants[0] >= 0:
			x1, _ = (a - 2*b + c - sqrt(discriminants[0])) \
				/ divisor
			x2, _ = (a - 2*b + c + sqrt(discrimiants[0])) \
				/ divisor
			x += [x1, x2]
		
		y = [self.pos_vec[1], other.pos_vec[1]]
		if discriminants[1] >= 0:
			_, y1 = (a - 2*b + c - sqrt(discriminants[1])) \
				/ divisor
			_, y2 = (a - 2*b + c + sqrt(discrimiants[1])) \
				/ divisor
			y += [y1, y2]
			
		return (min(x), min(y), max(x), max(y))
			
			
			
			
			
			
			
			