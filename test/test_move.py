"""
运动物体仿真.
"""

import unittest
import numpy as np
from simu import Environment, MoveEntity
from simu import vec


def print_position(bird):
    print('{:.2f} : {}  - {}'.format(bird.env.time_info[0], vec.to_str(bird.position), bird.track.is_over()))


class MoveTest(unittest.TestCase):
    def test_move_entity(self):
        """ 测试 MoveEntity 基本操作."""
        env = Environment()
        bird = MoveEntity(name='bird', speed=5, waypoints=[[1, 1], [10, 10]])
        bird.step_events.append(print_position)
        np.testing.assert_almost_equal(bird.track.start, vec.array([1, 1]))
        np.testing.assert_almost_equal(bird.track.end, vec.array([10, 10]))

        env.add(bird)
        np.testing.assert_almost_equal(bird.position, bird.track.start)

        env.run(duration=5)
        np.testing.assert_almost_equal(bird.position, bird.track.end)
        self.assertTrue(True)
