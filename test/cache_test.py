import unittest
from utils.cache import RedisManager


class TestRedisManager(unittest.TestCase):
    def test_set(self):
        self.assertTrue(RedisManager.set('test_key', 'test_value', 3600))

    def test_get(self):
        RedisManager.set('test_key', 'test_value', 3600)
        self.assertEqual(RedisManager.get('test_key'), 'test_value')

    def test_delete(self):
        RedisManager.set('test_key', 'test_value', 3600)
        self.assertTrue(RedisManager.delete('test_key'))
        self.assertIsNone(RedisManager.get('test_key'))


if __name__ == '__main__':
    unittest.main()