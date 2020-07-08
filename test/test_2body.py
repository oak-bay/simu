""" 
二体运动仿真.
"""

import unittest
from simu import Environment, Entity
from simu import vec
import numpy as np

K = 9.8


def gravaity_rule(obj, other):
    """ 万有引力定律. """
    v = vec.unit(obj.pos - other.pos)
    a = K * other.M * (vec.dist(obj.pos, other.pos) ** 2)
    obj.F = obj.F + a * v


class Body(Entity):
    """ 运动物体. """

    def __init__(self, name=''):
        super().__init__(name)
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


class Recorder:
    def __init__(self):
        self.pos1 = []
        self.pos2 = []

    def __call__(self, env):
        sat = env.find('sat')
        if sat:
            self.pos1.append(sat.pos)

        earth = env.find('earth')
        if earth:
            self.pos2.append(earth.pos)


if __name__ == '__main__':
    env = Environment()
    env.step_events.append(Recorder())

    sat = env.add(Body('sat'))
    sat.pos = np.array([0, 1000], dtype=np.float)
    sat.vel = np.array([10, 0], dtype=np.float)

    earth = env.add(Body('earth'))
    earth.M = 1e6

    env.run(step=1.0, duration=300)
