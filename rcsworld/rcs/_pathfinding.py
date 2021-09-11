from queue import PriorityQueue
from typing import Tuple, List, Dict

from .blocks import RailBlock

QueuedNode = Tuple[float, float, RailBlock]  # Total_cost, distance, block


def heuristic(block: RailBlock, end_block: RailBlock) -> float:
    # Use squared euclidean distance
    x, y = block.center
    tx, ty = end_block.center
    return (x - tx)**2 + (y - ty)**2


def travel_cost(block: RailBlock) -> float:
    pass  # TODO


def a_star(start_block: RailBlock, end_block: RailBlock) -> List[RailBlock]:
    queue: PriorityQueue[QueuedNode] = PriorityQueue()
    queue.put((heuristic(start_block, end_block), 0, start_block))

    prev_blocks: Dict[RailBlock, RailBlock] = {end_block: None}

    while not queue.empty():
        _, distance, block = queue.get()

        if block == end_block:
            break

        previous_block = prev_blocks[block]
        next_blocks = block.next_blocks(previous_block)

        for next_block in next_blocks:
            extra_distance = travel_cost(next_block)
            cost = distance + extra_distance + heuristic(next_block, end_block)

            if next_block in prev_blocks:
                pass  # maybe a better path has been found, but this should
                # never occur on a grid
            else:
                prev_blocks[next_block] = block
                queue.put((cost, distance + extra_distance, next_block))

    path = [end_block]
    block = end_block
    while block != start_block:
        block = prev_blocks[block]
        path.append(block)

    return path



