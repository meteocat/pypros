import unittest
from pypros.pros import calculate_koistinen_saltikoff
from pypros.pros import calculate_pros
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

    def test_calculate_pros(self):

        temp = numpy.ones((3, 6))
        tempd = numpy.ones((3, 6))
        refl = numpy.ones((3, 6))

        refl_values = [0.2, 2, 6, 12, 16, 26]
        for i in range(6):
            temp[0][i] = 20
            tempd[0][i] = 20
            temp[1][i] = 2
            tempd[1][i] = 0
            temp[2][i] = -1
            tempd[2][i] = -1
            refl[0][i] = refl_values[i]
            refl[1][i] = refl_values[i]
            refl[2][i] = refl_values[i]

        result = calculate_pros(temp, tempd, refl)

        # With a reflectivity < 1, value is 0
        for i in range(3):
            self.assertEqual(result[i][0], 0)

        # rain
        for i in range(1, 6):
            self.assertEqual(result[0][i], i)
        # sleet
        for i in range(1, 6):
            self.assertEqual(result[1][i], 5 + i)
        # snow
        for i in range(1, 6):
            self.assertEqual(result[2][i], 10 + i)

        # Check non numpy values
        result = calculate_pros(2, 0, 12)
        self.assertEqual(result, 8)

        # Check wet bulb method
        result = calculate_pros(2, 0, 12, method='tw')
        self.assertEqual(result, 13)
        result = calculate_pros(6, 0, 12, method='tw')
        self.assertEqual(result, 3)

        with self.assertRaises(IndexError) as cm:
            calculate_pros(23, tempd, numpy.ones((3, 5)))
        self.assertEqual(
            "The three parameters must have the same type",
            str(cm.exception))

        with self.assertRaises(IndexError) as cm:
            calculate_pros(temp, tempd, numpy.ones((3, 5)))
        self.assertEqual(
            "The matrices must have the same dimensions",
            str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            calculate_pros(temp, tempd, refl, method='fake')
        self.assertEqual(
            "Non valid method. Valid values are ks and tw",
            str(cm.exception))


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
