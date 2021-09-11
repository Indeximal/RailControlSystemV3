from .joint import RailJoint
from .block import RailBlock

def example_usage():
	loop = (RailNetworkBuilder()
		.start(0, -1)
		.mark("start")
		.track_to(1, 0)
		.track_to(0, 1)
		.track_to(-1, 0)
		.connect_to("start")
		.build())
	
	network = (RailNetworkBuilder()
		.start(-1, 1)
		.mark("start")
		.track_to(0, 0)
		.split()
		.track_to(2, 1)
		.track_to(0, 3)
		.mark("A")
		.build_other()
		.track_to(1, 1)
		.merge_into("A")
		.connect_to("start")
		.build())

	return network


class RailNetwork:
	def __init__(self):
		self.joint_connections_right = dict()
		self.joint_connections_left = dict()
		self.blocks = list()
		
	def connect(self, joint_a: RailJoint, joint_b: RailJoint) -> RailBlock:
		block = RailBlock(joint_a, joint_b)
		# TODO: maybe implement this?
		return block
			


class RailNetworkBuilder:
	def __init__(self):
		self.network: RailNetwork = RailNetwork()
		self.prev_joint = None
		self.prev_track = None
		self.marks = dict()
	
	def start(self, x: float, y: float):
		self.prev_joint = RailJoint(x, y, 0)
		return self
		
	def mark(self, mark_name: str):
		self.marks[mark_name] = self.prev_joint
		return self
		
	def track_to(self, x: float, y: float):
		joint = RailJoint(x, y, 0)
		track = RailBlock(self.prev_joint, joint)
		
		if self.prev_track:
			self.prev_track.b_connections.append(track)
			track.a_connections = [self.prev_track]
			
		self.network.blocks.append(track)
		
		self.prev_joint = joint
		self.prev_track = track
		return self
		
	def connect_to(self, mark_name: str):
		joint = self.marks[mark_name]
		track = RailBlock(self.prev_joint, joint)
		
		if self.prev_track:
			self.prev_track.b_connections.append(track)
			track.a_connections = [self.prev_track]
			

		next_track = None
		for block in self.network.blocks:
			if joint == block.a_joint:
				next_track = block
				break
		
		if not next_track:
			raise Exception("Coundn't find track to connect to")
	
		track.b_connections = [next_track]
		next_track.a_connections.append(track)		
			
		self.network.blocks.append(track)
		
		self.prev_joint = None
		self.prev_track = None
		return self
		
	def build(self):
		return self.network
	
		
	

	