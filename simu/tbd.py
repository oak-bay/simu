from simu import Entity
from simu import vec


class DetectResult:
    """ 检测结果. """

    def __init__(self, parent):
        self.parent = parent
        self.results = {}  # dict[id, (time, batch_id, result)]
        self.batch_id = 0
        self.update_interval = 1.0
        self.remove_interval = 3.0

    def accept(self, target, result):
        assert (result is not None)
        now = self.parent.time_info[0] if self.parent.time_info else None
        prev = self._get_prev_time(target)
        if now is not None and prev is not None and self.update_interval > 0 and now - prev < self.update_interval:
            return

        if target.id in self.results:
            _, batch_id, _ = self.results[target.id]
            self.results[target.id] = now, batch_id, result
        else:
            self.batch_id += 1
            self.results[target.id] = now, self.batch_id, result

    def _get_prev_time(self, target):
        if target.id in self.results:
            return self.results[target.id][0]
        return None

    def reset(self):
        self.batch_id = 0
        self.results.clear()

    def step(self, time_info):
        if self.remove_interval > 0:
            now = time_info[0]
            keys = []
            for k, v in self.results.items():
                t = v[0]
                if (t is not None) and (now - t > self.remove_interval):
                    keys.append(k)
            for k in keys:
                self.results.pop(k)


class Detector:
    """ 检测器.  """

    def __init__(self, parent):
        self.parent = parent
        self.detect_filters = []

    def detect(self, target: Entity):
        """ 检测目标. """
        assert (self.parent is not None)
        ret = 0
        for fil in self.detect_filters:
            ret = fil(self, target, ret)
            if ret is None:
                return None
        return ret

    def reset(self):
        pass

    def step(self, time_info):
        pass

    @property
    def position(self):
        return self.parent.position


def detect_rcs_pos(detector: Detector, target: Entity, ret):
    """ 检查目标是否具有位置属性. """
    if hasattr(target, 'position'):  # and hasattr(target, 'rcs'):
        return ret
    return None


def detect_rel_pos(detector: Detector, target: Entity, ret):
    """ 测量目标相对位置. """
    return target.position - detector.position


def detect_aer(detector: Detector, target: Entity, ret):
    """ 测量目标的AER值. """
    rel_pos = target.position - detector.position
    return vec.cart_to_pole(rel_pos, fmt='d')


class Radar(Entity):
    """ 雷达. """

    def __init__(self, name='', **kwargs):
        super().__init__(name)
        self.position = vec.array([0, 0])
        self.access_handlers.append(Radar.detect)
        self.result = DetectResult(self)
        self.detector = Detector(self)
        self.detector.detect_filters.append(detect_rcs_pos)
        self.detector.detect_filters.append(detect_aer)
        self.set_values(**kwargs)

    def set_values(self, **kwargs):
        if 'position' in kwargs:
            self.position = kwargs['position']

    def reset(self):
        self.result.reset()
        self.detector.reset()

    def step(self, time_info):
        super().step(time_info)
        self.detector.step(time_info)
        self.result.step(time_info)

    def detect(self, target):
        result = self.detector.detect(target)
        if result is not None:
            self.result.accept(target, result)

    @property
    def results(self):
        assert (self.result is not None)
        return self.result.results
