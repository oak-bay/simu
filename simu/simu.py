from typing import List, Tuple
import time


class Entity(object):
    """ 仿真实体.
    """

    _GlobalId: int = 0  # 全局 ID 计数器.

    @classmethod
    def _gen_entity_id(cls) -> int:
        Entity._GlobalId += 1
        return Entity._GlobalId

    def __init__(self):
        self._env = None  # Environment
        self._id = Entity._gen_entity_id()
        self.name = ''

    @property
    def id(self) -> int:
        return self._id

    def attach(self, env):
        self._env = env

    def reset(self):
        pass

    def step(self, time_info):
        pass


class Environment(object):
    """ 仿真环境.

    1.实体管理功能.
    2.仿真管理功能. 
    """

    def __init__(self):
        self._entities = []  # List[Entity]
        self._clock = _SimClock()

    def run(self, **kwargs):
        """ 连续运行. """
        self.reset(**kwargs)
        while not self.is_over():
            self.step()

    def reset(self, **kwargs):
        """ 重置. """
        self._clock.reset(**kwargs)
        for obj in self._entities:
            obj.reset()

    def step(self):
        """ 步进. """
        time_info = self._clock.step()
        for obj in self._entities:
            obj.step(time_info)

    def is_over(self) -> bool:
        """ 判断是否结束. """
        return self._clock.is_over()

    @property
    def entities(self):
        """ 仿真环境中实体列表. """
        return self._entities

    def add(self, obj: Entity):
        """ 添加仿真实体. 
        
        :param obj: 需要加入环境的仿真实体.
        :return: 已经加入环境的仿真实体.
        """
        if self.find(obj) is None:
            obj.attach(self)
            self._entities.append(obj)
            return obj
        return None

    def remove(self, obj_tag):
        """ 删除仿真实体. 

        :param obj_tag: 仿真实体的标签，对象 | ID | Name
        """
        for i, obj in enumerate(self._entities):
            if self._compare_obj_tag(obj, obj_tag):
                obj.attach(None)
                del self._entities[i]
                break

    def find(self, obj_tag) -> Entity:
        """ 查找仿真实体.

        :param obj_tag: 仿真实体的标签，对象 | ID | Name
        :return: 如果找到，返回仿真实体；否则返回 None.         
        """
        for obj in self._entities:
            if self._compare_obj_tag(obj, obj_tag):
                return obj
        return None

    @property
    def time_info(self):
        return self._clock.time_info

    def _compare_obj_tag(self, obj, obj_tag) -> bool:
        """ 检查对象和标签是否相符 """
        if isinstance(obj_tag, Entity):
            return obj is obj_tag
        if isinstance(obj_tag, int):
            return obj.id == obj_tag
        if isinstance(obj_tag, str) and obj_tag != '':
            return obj.name == obj_tag
        return False


class _SimClock(object):
    """ 仿真时钟. 
    
    TODO: 考虑运行时间的设置.
    """

    def __init__(self, start=0., duration=10., step=0.1, realtime=False):
        """ 初始化时钟.

        :param step: 仿真步长.
        :param start: 仿真起始时间.
        :param duration: 仿真持续时长.
        :param realtime: 是否实时仿真.
        """
        self._step = step
        self._range = [start, start + duration]
        self._now = 0.

        self.realtime = realtime
        self._prev_t = None

        self.reset()

    def set_values(self, **kwargs):
        """ 设置参数值. """
        if 'step' in kwargs:
            self._step = float(kwargs['step'])
        if 'start' in kwargs:
            self._range[0] = float(kwargs['start'])
        if 'duration' in kwargs:
            self._range[1] = self._range[0] + float(kwargs['duration'])
        if 'realtime' in kwargs:
            self.realtime = bool(kwargs['realtime'])

    def reset(self, **kwargs):
        """ 重置. """
        self.set_values(**kwargs)
        self._now = self._range[0]
        self._prev_t = None

    def step(self) -> Tuple[float, float]:
        """ 步进. """
        self._now += self._step
        self.wait_for_realtime()
        return self.time_info

    def wait_for_realtime(self):
        """ 同步. """
        if self.realtime:
            if self._prev_t is None:
                self._prev_t = time.time()
            else:
                real_t = time.time() - self._prev_t
                # dt = self._step - real_t
                dt = (self._now - self._range[0]) - real_t
                if dt > 0.:
                    time.sleep(dt)
                # self._prev_t = time.time()

    def is_over(self) -> bool:
        """ 判断时钟是否结束. """
        return self._now >= self._range[1]

    @property
    def time_info(self) -> Tuple[float, float]:
        """ 当前时钟信息. """
        return self._now, self._step
