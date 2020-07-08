import numpy
import math


def to_str(v, fmt='%.3f') -> str:
    """ 将数组（）转换为字符串. """
    values = [fmt % e for e in v]
    ret = ', '.join(values)
    return '[' + ret + ']'


def is_equal(v0, v1) -> bool:
    """ 判断向量是否内容相等. """
    return (array(v0) == array(v1)).all()


def is_close(v0, v1, atol=1e-8) -> bool:
    """ 判断向量是否内容相近. """
    return numpy.allclose(array(v0), array(v1), atol=atol)


def dist(v1, v0=None) -> float:
    """ 计算向量长度. """
    a = array(v1)
    return numpy.linalg.norm(a) if v0 is None else numpy.linalg.norm(a - array(v0))


def unit(v) -> numpy.ndarray:
    """ 计算单位向量.
    """
    a = array(v)
    d = dist(a)
    return a / d if d > 0. else numpy.zeros(a.shape, numpy.float)


def array(v) -> numpy.ndarray:
    """ 向量化. """
    return v if isinstance(v, numpy.ndarray) else numpy.array(v, numpy.float)


def proj(v1, v0) -> numpy.ndarray:
    """ 向量投影.

    将向量 v1 投影至 v0.
    """
    a = v1 if isinstance(v1, numpy.ndarray) else numpy.array(v1, numpy.float)
    b = unit(v0)
    return b * numpy.dot(a, b)


def angle(v0, v1, fmt='d') -> float:
    """ 计算向量夹角.

    :param v0: 向量1.
    :param v1: 向量2.
    :param fmt: 返回值格式. 默认是度数.
            'd', 'degree' : 度数.
            'r', 'radian' : 弧度.
    """
    v0_, v1_ = array(v0), array(v1)
    d0, d1 = dist(v0_), dist(v1_)
    if d0 > 0. and d1 > 0.:
        v = numpy.dot(v1_, v0_) / d0 / d1
        a = math.acos(v)
        if fmt in ('d', 'degree'):
            return math.degrees(a)
        elif fmt in ('r', 'radian'):
            return a
        else:
            raise Exception("fmt parameter: invalid value.")
    else:
        return float(0)


def aer_to_xyz(aer, center=None, fmt='d') -> numpy.ndarray:
    """ AER坐标 转换至 XYZ坐标.

    :param aer: aer 坐标.
    :param center: 极坐标中心点坐标.
    :param fmt: 角度格式. 默认是度数.
            'd', 'degree' : 度数.
            'r', 'radian' : 弧度.
    :return: xyz 坐标.
    """
    if fmt in ('r', 'radian'):
        a, e, r = aer[0], aer[1], aer[2]
    elif fmt in ('d', 'degree'):
        a, e, r = math.radians(aer[0]), math.radians(aer[1]), aer[2]
    else:
        raise Exception("fmt parameter: invalid value.")
    z = r * math.sin(e)
    r2 = r * math.cos(e)
    x, y = r2 * math.sin(a), r2 * math.cos(a)

    ret = numpy.array([x, y, z], dtype=numpy.float)
    if center is not None:
        ret = ret + array(center)
    return ret


def xyz_to_aer(xyz, center, fmt='d') -> numpy.ndarray:
    """ XYZ坐标 转换至 AER坐标.

    :param xyz: xyz 坐标.
    :param center: 中心点坐标.
    :param fmt: 角度格式. 默认是度数.
            'd', 'degree' : 度数.
            'r', 'radian' : 弧度.
    :return: aer 坐标.
    """
    xyz2 = xyz if center is None else (xyz - center)
    r = dist(xyz2)
    if r > 0.:
        r2 = dist(xyz2[0:2])
        a = math.atan2(xyz2[0], xyz2[1])
        e = math.atan2(xyz2[2], r2)
        if fmt in ('d', 'degree'):
            a = math.degrees(a) % 360
            e = math.degrees(e)
        return numpy.array([a, e, r], dtype=numpy.float)
    else:
        return numpy.array([0, 0, 0], dtype=numpy.float)
