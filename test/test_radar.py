"""
雷达测试.
"""

import unittest
import numpy as np
from simu import Environment
from simu.common import MoveEntity
from simu.tbd import Radar


def radar_result_report(radar):
    for k, v in radar.results.items():
        t, b, r = v
        if t == radar.time_info[0]:
            print(k, v)


class RadarTest(unittest.TestCase):
    def test_create(self):
        env = Environment()
        radar = env.add(Radar())
        env.run()
        self.assertTrue(True)

    def test_detect(self):
        env = Environment()
        radar = env.add(Radar(position=[0, 0, 0]))
        radar.step_events.append(radar_result_report)
        bird = env.add(MoveEntity(name='bird', speed=5,
                                  waypoints=[[1, 1, 1], [10, 10, 10]]))
        env.run(duration=30)
        self.assertTrue(True)
