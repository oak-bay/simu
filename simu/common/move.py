import numpy as np

from simu import Entity
from simu import vec


class Track(object):
    """ 航线. """

    def __init__(self, dim=2, **kwargs):
        self.dim = max(int(dim), 2)
        self.waypoints = []
        self.set_values(**kwargs)
        self._index = 0

    def set_values(self, **kwargs):
        if 'waypoints' in kwargs:
            self.waypoints.clear()
            for val in kwargs['waypoints']:
                self.waypoints.append(vec.array(val))

    def reset(self):
        self._index = 0

    def is_over(self):
        return (self._index + 1) >= len(self.waypoints)

    def move(self, pos, dist) -> np.ndarray:
        curr = pos.copy()
        while dist > 0:
            # 获取当前目标点.
            target = self._get_target()
            if np.allclose(curr, target):
                break
            # 移动当前位置.
            d = vec.dist(curr, target)
            if dist <= d:
                curr += dist / d * (target - curr)
                break
            else:
                curr = target
                dist -= d
                self._index += 1
        return curr

    def _get_target(self) -> np.ndarray:
        target_index = self._index + 1
        if target_index >= len(self.waypoints):
            return self.end
        return self.waypoints[target_index]

    @property
    def start(self):
        """ 起点. """
        return self.waypoints[0] if self.waypoints else np.zeros(self.dim)

    @property
    def end(self):
        """ 终点. """
        return self.waypoints[-1] if self.waypoints else np.zeros(self.dim)


class MoveEntity(Entity):
    """ 运动物体.

    Attributes:
        position: 当前位置.
        velocity: 瞬时速度（向量）.
        speed: 速度.
    """

    def __init__(self, name='', **kwargs):
        super().__init__(name)
        self.protect_props.extend(['position', 'velocity'])
        # 设置默认值.
        self.track = Track()
        self.position = np.zeros(2)
        self.velocity = np.zeros_like(self.position)
        self.speed = 1.0
        self.auto_active = True
        self.step_handlers.append(MoveEntity.move)
        # 进行相应初始化.
        self.set_values(**kwargs)
        self.reset()

    def set_values(self, **kwargs):
        if 'speed' in kwargs:
            self.speed = float(kwargs['speed'])
        if 'waypoints' in kwargs:
            self.track.set_values(waypoints=kwargs['waypoints'])

    def reset(self):
        self.position = self.track.start
        self.velocity = np.zeros_like(self.position)
        self.track.reset()

    def move(self, time_info):
        prev_pos, dt = self.position, time_info[1]
        self.do_move(time_info)
        self.velocity = (self.position - prev_pos) / dt if dt > 0. \
            else np.zeros_like(self.position)
        if self.auto_active and np.allclose(self.position, self.track.end):
            self.set_active(False)

    def do_move(self, time_info):
        """ 移动位置. """
        self.position = self.track.move(
            self.position, self.speed * time_info[1])
