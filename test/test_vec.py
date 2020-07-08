from unittest import TestCase

import numpy as np
from simu import vec
from simu.vec import aer_to_xyz, xyz_to_aer, angle


class Test(TestCase):
    def test_xyz_and_aer(self):
        center = vec.array([1, 1, 1])
        xyz1 = vec.array([4, 5, 14])
        aer = xyz_to_aer(xyz1, center)
        xyz2 = aer_to_xyz(aer, center)
        np.testing.assert_array_almost_equal(xyz1, xyz2)

        center = vec.array([1, 1, 1])
        xyz1 = vec.array([4, 5, 14])
        aer = xyz_to_aer(xyz1, center, fmt='r')
        xyz2 = aer_to_xyz(aer, center, fmt='r')
        np.testing.assert_array_almost_equal(xyz1, xyz2)

        center = np.random.random(3)
        xyz1 = np.random.random(3)
        aer = xyz_to_aer(xyz1, center)
        xyz2 = aer_to_xyz(aer, center)
        np.testing.assert_array_almost_equal(xyz1, xyz2)

    def test_angle(self):
        pos1 = np.array([1, 0, 0])
        pos2 = np.array([1, 1, 0])
        a = angle(pos1, pos2)
        self.assertAlmostEqual(a, 45.)

        pos2 = np.array([0, 8, 0])
        self.assertAlmostEqual(angle(pos1, pos2), 90.)

        pos2 = np.array([-10, 0, 0])
        self.assertAlmostEqual(angle(pos1, pos2), 180.)

        pos2 = np.array([0, 0, 0])
        self.assertAlmostEqual(angle(pos1, pos2), 0.)

        # 随机测试.
        for _ in range(10):
            p1 = np.random.random(3) * 10
            p2 = np.random.random(3) * 10
            self.assertAlmostEqual(angle(p1, p2), angle(p2, p1))

    def test_array(self):
        v1 = np.array([0, 8, 0], np.float)
        v2 = vec.array(v1)
        self.assertEqual(id(v1), id(v2))

        v1 = [0, 8, 0]
        v2 = vec.array(v1)
        self.assertTrue(isinstance(v2, np.ndarray))

    def test_proj(self):
        v0 = vec.array([1, 1, 1])
        v1 = vec.array([4, 5, 14])
        v1_p = vec.proj(v1, v0)
        v1_v = v1 - v1_p
        self.assertAlmostEqual(np.dot(v1_p, v1_v), 0.)
        np.testing.assert_array_almost_equal(vec.unit(v0), vec.unit(v1_p))

        v = vec.proj([1, 1], [1, 0])
        np.testing.assert_almost_equal(v, [1, 0])

        v = vec.proj([1, 1], [-1, 0])
        np.testing.assert_almost_equal(v, [1, 0])

        v = vec.proj([1, 0], [1, 1])
        np.testing.assert_almost_equal(v, [0.5, 0.5])

        v = vec.proj([0, 1], [1, 1])
        np.testing.assert_almost_equal(v, [0.5, 0.5])

        v = vec.proj([1, 0], [2, 2])
        np.testing.assert_almost_equal(v, [0.5, 0.5])

    def test_dist(self):
        v = vec.dist([1, 0])
        self.assertAlmostEqual(v, 1.0)

        v = vec.dist([2, 0])
        self.assertAlmostEqual(v, 2.0)

        v = vec.dist([-2, 0])
        self.assertAlmostEqual(v, 2.0)

        v = vec.dist([-1, 1])
        self.assertAlmostEqual(v, 2 ** 0.5)

    def test_unit(self):
        v = vec.unit([1, 0])
        np.testing.assert_almost_equal(v, [1., 0])

        v = vec.unit([2, 0])
        np.testing.assert_almost_equal(v, [1., 0])

        v = vec.unit([-2, 0])
        np.testing.assert_almost_equal(v, [-1., 0])

        v = vec.unit([0, 0])
        np.testing.assert_almost_equal(v, [0, 0])
