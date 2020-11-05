import unittest
from BJTFeedback import *


class UnitTests1(unittest.TestCase):

    def test1(self):
        result = calc_bias(12, 22, 1500, 680, 47, 100)
        self.assertAlmostEqual(result["Ie"], 0.051, places=3)

    def testEMRFD_2_25(self):
        ssr = calc_small_signal(50, 1300, 1000, 6, 200, 0.020, 21)
        self.assertAlmostEqual(ssr["gain"], 20, places=0)


if __name__ == '__main__':
    unittest.main()