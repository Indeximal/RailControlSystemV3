from PIL import Image, ImageDraw
import numpy as np

from .network import RailNetwork, RailBlock


def draw_block_on(block: RailBlock, im: ImageDraw):
	T = np.linspace(0, 1, 10)
	points = [block.a_point.bezier_to(block.b_point, t) for t in T]
	transform = lambda p: tuple(p * 200 + 400)
	coords = [transform(point.pos_vec) for point in points]
	
	im.line(coords, (0, 0, 0, 255), 2)


def draw_network(network: RailNetwork):
	im = Image.new("RGBA", (800, 600), (255, 255, 255, 0))
	drawer = ImageDraw.Draw(im)
	
	for block in network.blocks:
		draw_block_on(block, drawer)
		
	return im
