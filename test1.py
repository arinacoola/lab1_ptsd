import unittest
from lab1 import euler_phi, generalized_euler_phi

class TestEulerFunctions(unittest.TestCase):

    def test_euler_phi(self):
        self.assertEqual(euler_phi(1), 1)
        self.assertEqual(euler_phi(2), 1)
        self.assertEqual(euler_phi(3), 2)
        self.assertEqual(euler_phi(4), 2)
        self.assertEqual(euler_phi(5), 4)
        self.assertEqual(euler_phi(10), 4)
        self.assertEqual(euler_phi(12), 4)
        self.assertEqual(euler_phi(30), 8)

    def test_generalized_euler_phi(self):
        self.assertEqual(generalized_euler_phi(1, 10), 1)
        self.assertEqual(generalized_euler_phi(10, 5), 4)
        self.assertEqual(generalized_euler_phi(12, 5), 4)

if __name__ == '__main__':
    unittest.main()
