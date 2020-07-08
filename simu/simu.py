from typing import List, Tuple


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

    def run(self):
        """ 连续运行. """
        self.reset()
        while not self.is_over():
            self.step()

    def reset(self):
        """ 重置. """
        self._clock.reset()
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
    """ 仿真时钟. """

    def __init__(self):
        """ 初始化时钟.

        TODO: 增加可选择初始化内容.
        """
        self._step = 0.1
        self.range = [0., 10.]

        self._now = 0.
        self.reset()

    def reset(self):
        """ 重置. """
        self._now = self.range[0]

    def step(self) -> Tuple[float, float]:
        """ 步进. """
        self._now += self._step
        return self.time_info

    def is_over(self) -> bool:
        """ 判断时钟是否结束. """
        return self._now >= self.range[1]

    @property
    def time_info(self) -> Tuple[float, float]:
        """ 当前时钟信息. """
        return self._now, self._step
