import unittest
from simu import Environment, Entity


class SimuTestCase(unittest.TestCase):
    def test_entity(self):
        """ 测试实体属性. """
        # 不同实体 ID 不同.
        obj1 = Entity()
        obj2 = Entity()
        self.assertTrue(obj1.id != obj2.id)

    def test_entity_manage(self):
        """ 测试实体管理. """
        env = Environment()

        obj1 = env.add(Entity())
        self.assertTrue(obj1 is not None)
        self.assertTrue(len(env.entities) == 1)

        env.add(obj1)
        self.assertTrue(len(env.entities) == 1)

        obj2 = env.add(Entity())
        self.assertTrue(obj2 is not None)
        self.assertTrue(len(env.entities) == 2)

        obj3 = env.add(Entity())
        self.assertTrue(obj3 is not None)
        self.assertTrue(len(env.entities) == 3)

        self.assertTrue(obj1.id != obj2.id != obj3.id)

        obj = env.find('hello')
        self.assertTrue(obj is None)

        obj = env.find(obj2.id)
        self.assertTrue(obj is obj2)

        env.remove(obj2.id)
        self.assertTrue(len(env.entities) == 2)

    def test_run(self):
        """ 测试场景运行. """
        env = Environment()
        env.add(Entity())

        # 测试连续运行.
        env.reset()
        self.assertAlmostEqual(env.time_info[0], 0.)
        env.run()
        self.assertAlmostEqual(env.time_info[0], 10.1, 3)
        self.assertTrue(env.is_over())

        # 测试单步运行.
        env.reset()
        self.assertAlmostEqual(env.time_info[0], 0.)
        env.step()
        self.assertAlmostEqual(env.time_info[0], 0.1)
        self.assertFalse(env.is_over())
        env.step()
        self.assertAlmostEqual(env.time_info[0], 0.2)
        self.assertFalse(env.is_over())
