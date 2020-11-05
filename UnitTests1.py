import unittest
from BJTFeedback import *


class UnitTests1(unittest.TestCase):

    def test_1(self):
        result = calc_bias(12, 22, 1500, 680, 47, 100)
        # self.assertEqual('foo'.upper(), 'FOO')
        print(result)


if __name__ == '__main__':
    unittest.main()