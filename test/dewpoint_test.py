import unittest
from pypros.dewpoint import td2hr
from pypros.dewpoint import hr2td
from pypros.dewpoint import ttd2tw
from pypros.dewpoint import trhp2tw
import numpy


class TestDewpoint(unittest.TestCase):
    def test_td2hr(self):
        '''
        http://www.wpc.ncep.noaa.gov/html/dewrh.shtml to calculate the values
        in a third party formula
        '''
        temp = numpy.ones((3, 1))
        tempd = numpy.ones((3, 1))

        temp[0][0] = 20
        tempd[0][0] = 20

        temp[1][0] = 20
        tempd[1][0] = 10

        temp[2][0] = 20
        tempd[2][0] = -10

        result = td2hr(temp, tempd)

        self.assertEqual(result[0][0], 100)
        self.assertEqual(round(result[1][0], 2), 52.57)
        self.assertEqual(round(result[2][0], 2), 12.26)

    def test_hr2td(self):
        '''
        http://www.wpc.ncep.noaa.gov/html/dewrh.shtml to calculate the values
        in a third party formula
        '''
        temp = numpy.ones((4, 1))
        r_h = numpy.ones((4, 1))

        temp[0][0] = 20
        r_h[0][0] = 100

        temp[1][0] = 20
        r_h[1][0] = 52.57

        temp[2][0] = 20
        r_h[2][0] = 88.29

        temp[3][0] = 20
        r_h[3][0] = 26.18

        result = hr2td(temp, r_h)

        self.assertTrue(abs(result[0][0] - 20) < 0.1)
        self.assertTrue(abs(result[1][0] - 10) < 0.1)
        self.assertTrue(abs(result[2][0] - 18) < 0.1)
        self.assertTrue(abs(result[3][0] - 0) < 0.1)

    def test_ttd2tw(self):
        '''
        Values checked at https://www.kwangu.com/work/psychrometric.htm
        For an independent result
        '''
        result = ttd2tw(20, 20)
        self.assertTrue(abs(result - 20.01019) < 0.1)
        temp = numpy.ones((3, 1))
        tempd = numpy.ones((3, 1))

        temp[0][0] = 20
        tempd[0][0] = 20

        temp[1][0] = 20
        tempd[1][0] = 10

        temp[2][0] = 20
        tempd[2][0] = -10

        result = ttd2tw(temp, tempd)
        self.assertTrue(abs(result[0][0] - 20.01019) < 0.1)
        self.assertTrue(abs(result[1][0] - 14.13) < 0.1)
        self.assertTrue(abs(result[2][0] - 7.79) < 0.5)  # Divergence at low rh

    def test_trhp2tw(self):
        '''
        Values checked at https://www.weather.gov/epz/wxcalc_rh
        For an independent result
        '''

        temp = numpy.ones((4, 1))
        r_h = numpy.ones((4, 1))
        p = numpy.ones((4, 1))

        temp[0][0] = 20
        r_h[0][0] = 100
        p[0][0] = 1013.25

        temp[1][0] = 20
        r_h[1][0] = 52.57
        p[1][0] = 1013.25

        temp[2][0] = 20
        r_h[2][0] = 88.29
        p[2][0] = 1013.25

        temp[3][0] = 20
        r_h[3][0] = 26.18
        p[3][0] = 1013.25

        result = trhp2tw(temp, r_h, p)

        self.assertEqual(result.shape[0], temp.shape[0])
        self.assertEqual(result.shape[1], temp.shape[1])

        self.assertAlmostEqual(result[0][0], 19.999, 2)
        self.assertAlmostEqual(result[1][0], 14.226, 2)
        self.assertAlmostEqual(result[2][0], 18.684, 2)
        self.assertAlmostEqual(result[3][0], 10.407, 2)


if __name__ == '__main__':
    unittest.main()
