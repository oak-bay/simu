""" 
二体运动仿真.
"""

import unittest
import matplotlib.pyplot as plt
import numpy as np
from simu import Environment, Entity
from simu import vec


class Body(Entity):
    """ 运动物体. """

    def __init__(self, name=''):
        super().__init__(name)
        self.protect_props.append('pos')
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.m = 1.
        self._f = np.zeros(2)

    def step(self, time_info):
        """ 步进. """
        _, dt = time_info
        self.vel += dt * self._f
        self.pos += self.vel * dt
        self._f = np.zeros(2)


def gravaity_rule(obj: Body, other: Body):
    """ 万有引力定律. """
    G = 6.67e-11  #
    v = vec.unit(other.pos - obj.pos)
    f = G * other.m / (vec.dist(obj.pos, other.pos) ** 2)
    obj._f += f * v


def chase_rule(obj: Body, other: Body):
    """ 追逐规律. """
    d = 1.5  # vec.dist(obj.vel)
    v = vec.unit(other.pos - obj.pos)
    obj.vel = d * v


class Recorder:
    """ 属性记录. """

    def __init__(self):
        self.records = {}

    def __call__(self, env):
        for obj in env.entities:
            if isinstance(obj, Body):
                if obj.id not in self.records:
                    self.records[obj.id] = []
                self.records[obj.id].append(obj.pos.copy())

    def plot(self, delay=1):
        plt.figure()
        for _, pos in self.records.items():
            xy = np.copy(np.array(pos).T)
            plt.plot(xy[0, :], xy[1, :])
        plt.axis('equal')
        plt.pause(delay)
        plt.close()


class BodyTest(unittest.TestCase):
    def test_earth_and_sat(self):
        env = Environment()
        recorder = Recorder()
        env.step_events.append(recorder)

        sat = env.add(Body('sat'))
        sat.pos = np.array([0, 6000e3], dtype=np.float)
        sat.vel = np.array([10e3, 0], dtype=np.float)
        sat.access_handlers.append(gravaity_rule)

        earth = env.add(Body('earth'))
        earth.access_handlers.append(gravaity_rule)
        earth.m = 5.965e24

        env.run(step=1.0, duration=30000)
        self.assertTrue(len(recorder.records) > 0)
        recorder.plot()

    def test_chase(self):
        """ 狗追兔子. """
        env = Environment()
        recorder = Recorder()
        env.step_events.append(recorder)

        rabbit = env.add(Body('rabbit'))
        rabbit.vel = np.array([1, 0], dtype=np.float)

        dog = env.add(Body('dog'))
        dog.pos = np.array([0, 20], dtype=np.float)
        dog.access_handlers.append(chase_rule)

        env.run(step=0.1, duration=30)
        self.assertTrue(len(recorder.records) > 0)
        recorder.plot()
