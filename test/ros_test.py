import unittest
from pypros.ros import calculate_koistinen_saltikoff
import numpy


class TestCalculateRos(unittest.TestCase):
    def test_calculate_koistinen_saltikoff(self):
        temp = numpy.ones((3, 1))
        tempd = numpy.ones((3, 1))

        temp[0][0] = 20
        tempd[0][0] = 20

        temp[1][0] = 2
        tempd[1][0] = 0

        temp[2][0] = -1
        tempd[2][0] = -1

        result = calculate_koistinen_saltikoff(temp, tempd)

        for i in range(temp.shape[0]):
            self.assertEqual(result[i][0], css(temp[i][0], tempd[i][0]))


def css(temp, tempd):
    '''
    Calculates the original koistinen_saltikoff
    '''
    es = 6.11 * 10**(7.5*tempd/(237.7+tempd))
    e = 6.11 * 10**(7.5*temp/(237.7+temp))

    hr = 100*(es/e)
    return 1 - 1/(1+pow(2.7182818, 22.-2.7*temp-0.2*hr))

if __name__ == '__main__':
    unittest.main()
