"""
运动物体仿真.
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
from simu import Environment
from simu.common import MoveEntity
from simu import vec


def print_position(bird):
    print('{:.2f} : {}  - {}'.format(
        bird.env.time_info[0], vec.to_str(bird.position), bird.track.is_over()))


def plot_records(records: list):
    if records:
        pt = records[-1]
        plt.plot(pt[0], pt[1], 'r*')


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

    def test_move_and_plot(self):
        """ 测试 MoveEntity 和绘制. """
        env = Environment()
        bird = env.add(MoveEntity(name='bird', speed=5,
                                  waypoints=[[1, 1], [10, 10]]))

        plt.figure(1)
        plt.axis([0, 20, 0, 20])  # plt.xlim((0, 20)), plt.ylim((0, 20))
        plt.ion()
        records = []
        env.reset()
        while not env.is_over():
            env.step()
            records.append(bird.position)
            plot_records(records)
            plt.pause(0.05)
        plt.close()

        np.testing.assert_almost_equal(bird.position, bird.track.end)
        self.assertTrue(True)
