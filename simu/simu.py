from typing import List, Tuple
import time
import copy


class Entity(object):
    """ 仿真实体.

    Attributes:
        id: ID.
        name: 名字[可选].
        env: 实体所绑定的环境.
        step_handlers: 步进处理函数列表.
            步进处理函数原型 step_handler(obj, time_info)
        access_handlers: 互操作处理函数列表.
            互操作处理函数原型 access_handler(obj, other)
    """

    _GlobalId: int = 0  # 全局 ID 计数器.

    @classmethod
    def _gen_entity_id(cls) -> int:
        """ 生成实体 ID. """
        Entity._GlobalId += 1
        return Entity._GlobalId

    def __init__(self, name=''):
        self.env = None  # Environment
        self._id = Entity._gen_entity_id()
        self.name = name
        self.step_handlers = []  # List
        self.step_events = []  # List
        self.access_handlers = []  # List

    @property
    def id(self) -> int:
        """ 实体 ID. """
        return self._id

    def attach(self, env):
        """ 绑定运行环境. """
        self.env = env

    def reset(self):
        """ 重置实体. """
        pass

    def step(self, time_info):
        """ 步进. """
        for handler in self.step_handlers:
            handler(self, time_info)

    def on_step(self):
        """ 处理步进消息. """
        for evt in self.step_events:
            evt(self)

    def access(self, others: List):
        """ 与其他实体交互. """
        for other in others:
            for handler in self.access_handlers:
                handler(self, other)

    def is_active(self) -> bool:
        """ 是否处于活动状态（是否参与仿真）"""
        return True


class Environment(object):
    """ 仿真环境.

    1.实体管理功能.
        add, remove, find
    2.仿真管理功能. 
        reset, run, step

    Attributes:
        step_evnets: 步进处理函数列表.
            步进处理函数原型 step_event(env)
    """

    def __init__(self):
        self._entities = []  # List[Entity]
        self._clock = _SimClock()
        self.step_events = []

    def __deepcopy__(self, memodict={}):
        """ 对象深拷贝.

        为保证性能，采用策略：整体浅拷贝，保护值深拷贝.
        通过指定 protect 属性，确认需要默认深拷贝的属性.
        """
        obj = copy.copy(self)
        return obj

    def run(self, **kwargs):
        """ 连续运行. """
        self.reset(**kwargs)
        while not self.is_over():
            self.step()

    def reset(self, **kwargs):
        """ 重置. """
        self._clock.set_values(**kwargs)
        self._clock.reset()
        for obj in self._entities:
            obj.reset()

    def step(self) -> bool:
        """ 步进. """
        time_info = self.time_info
        active_entities = [obj for obj in self._entities if obj.is_active()]

        # 互操作.
        mirror_entities = copy.deepcopy(active_entities)
        for obj in mirror_entities:
            others = [other for other in mirror_entities if other is not obj]
            obj.access(others)

        # 状态步进.
        for obj in active_entities:
            obj.step(time_info)

        # 处理步进事件.
        for evt in self.step_events:
            evt(self)

        self._clock.step()
        return self.is_over()

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

    def reset(self):
        """ 重置. """
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
        end = self._range[1]
        return (self._now >= end) or (abs(self._now - end) < 0.01 * self._step)

    @property
    def time_info(self) -> Tuple[float, float]:
        """ 当前时钟信息. 

        :return: Tuple[ 当前时刻，步进时间（从上一步到当前时刻）]
                当前时刻等于起始时，步进时间为 0；其他时间的步进为仿真步长.
        """
        return (self._now, self._step) if self._now > self._range[0] else (self._now, 0.)
