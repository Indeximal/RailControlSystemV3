from typing import Tuple

import numpy as np


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
