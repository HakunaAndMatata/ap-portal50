import unittest

class TestBasics(unittest.TestCase):

    def sample_test(self):
        self.assertEqual(14*2, 28)

if __name__ == '__main__':
    unittest.main()
