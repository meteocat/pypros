import unittest
from pypros.ros_methods import calculate_koistinen_saltikoff
from pypros.ros_methods import calculate_static_threshold
from pypros.ros_methods import calculate_linear_transition
from numpy import ones


class TestCalculateRosMethods(unittest.TestCase):
    def test_calculate_koistinen_saltikoff(self):
        temp = ones((3, 1))
        tempd = ones((3, 1))

        temp[0][0] = 20
        tempd[0][0] = 20

        temp[1][0] = 2
        tempd[1][0] = 0

        temp[2][0] = -1
        tempd[2][0] = -1

        result = calculate_koistinen_saltikoff(temp, tempd)

        for i in range(temp.shape[0]):
            self.assertEqual(result[i][0], ks_rh(temp[i][0], tempd[i][0]))

    def test_calculate_static_threshold(self):
        field = ones((3, 1))

        field[0][0] = 0.6
        field[1][0] = 2.3
        field[2][0] = 1.5

        result = calculate_static_threshold(field, 1.5)

        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[1][0], 0)
        self.assertEqual(result[2][0], 1)

    def test_calculate_linear_transition(self):
        field = ones((5, 1))

        field[0][0] = -0.6
        field[1][0] = 2.3
        field[2][0] = 1.0
        field[3][0] = 1.5
        field[4][0] = 0.1

        result = calculate_linear_transition(field, 0, 2)

        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[1][0], 0)
        self.assertEqual(result[2][0], 0.5)
        self.assertEqual(result[3][0], 0.25)
        self.assertEqual(result[4][0], 0.95)


def ks_rh(temp, tempd):
    """
    Calculates the original koistinen_saltikoff which uses
    relative humidity rather than dew point temperature.
    """
    es = 6.11 * 10**(7.5*tempd/(237.7+tempd))
    e = 6.11 * 10**(7.5*temp/(237.7+temp))

    hr = 100*(es/e)
    return 1 - 1/(1+pow(2.7182818, 22.-2.7*temp-0.2*hr))
