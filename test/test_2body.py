""" 
二体运动仿真.
"""

import unittest
from simu import Environment, Entity
from simu import vec
import numpy as np

K = 9.8  #


class Body(Entity):
    """ 运动物体. """

    def __init__(self, name=''):
        super().__init__(name)
        self.protect_props.append('pos')
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.M = 1.
        self._F = np.zeros(2)
        self.access_handlers.append(gravaity_rule)

    def step(self, time_info):
        """ 步进. """
        _, dt = time_info
        self.vel += dt * self._F
        self.pos += self.vel * dt
        self._F = np.zeros(2)


def gravaity_rule(obj: Body, other: Body):
    """ 万有引力定律. """
    v = vec.unit(other.pos - obj.pos)
    f = K * other.M / (vec.dist(obj.pos, other.pos) ** 2)
    obj._F += f * v
    pass


class Recorder:
    def __init__(self):
        self.pos1 = []
        self.pos2 = []

    def __call__(self, env):
        sat = env.find('sat')
        if sat:
            self.pos1.append(sat.pos.copy())

        earth = env.find('earth')
        if earth:
            self.pos2.append(earth.pos.copy())

    def plot(self):
        import matplotlib.pyplot as plt
        xy = np.array(self.pos1).T
        plt.plot(xy[0,:], xy[1,:], 'g')

        xy = np.array(self.pos2).T
        plt.plot(xy[0,:], xy[1,:], 'r')
        plt.show()


class BodyTest(unittest.TestCase):
    def test_earth_and_sat(self):
        env = Environment()
        recorder = Recorder()
        env.step_events.append(recorder)

        sat = env.add(Body('sat'))
        sat.pos = np.array([0, 1000], dtype=np.float)
        sat.vel = np.array([20, 0], dtype=np.float)

        earth = env.add(Body('earth'))
        earth.M = 1e3

        env.run(step=1.0, duration=3000)
        self.assertTrue(len(recorder.pos1) == len(recorder.pos2) > 0)
        recorder.plot()
