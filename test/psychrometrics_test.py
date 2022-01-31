import unittest
from pypros.psychrometrics import td2hr
from pypros.psychrometrics import hr2td
from pypros.psychrometrics import ttd2tw
from pypros.psychrometrics import trhp2tw
from pypros.psychrometrics import _get_p_from_z
from pypros.psychrometrics import get_tw_sadeghi
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

    def test_get_p_from_z(self):
        z = numpy.ones((4, 1))
        z[0][0] = 0
        z[1][0] = 630
        z[2][0] = 1500
        z[3][0] = 3000

        p = _get_p_from_z(z)

        self.assertAlmostEqual(p[0][0], 1013.25, 2)
        self.assertAlmostEqual(p[1][0], 940.80, 2)
        self.assertAlmostEqual(p[2][0], 850.63, 2)
        self.assertAlmostEqual(p[3][0], 718.15, 2)

    def test_trhp2tw(self):
        '''
        Values checked at https://www.weather.gov/epz/wxcalc_rh
        For an independent result
        '''
        temp = numpy.ones((4, 1))
        r_h = numpy.ones((4, 1))
        z = numpy.ones((4, 1))

        temp[0][0] = 20
        r_h[0][0] = 100
        z[0][0] = 0

        temp[1][0] = 20
        r_h[1][0] = 52.57
        z[1][0] = 630

        temp[2][0] = 20
        r_h[2][0] = 88.29
        z[2][0] = 1500

        temp[3][0] = 20
        r_h[3][0] = 26.18
        z[3][0] = 3000

        result = trhp2tw(temp, r_h, z)

        self.assertEqual(result.shape[0], temp.shape[0])
        self.assertEqual(result.shape[1], temp.shape[1])

        self.assertAlmostEqual(result[0][0], 20.000, 2)
        self.assertAlmostEqual(result[1][0], 14.057, 2)
        self.assertAlmostEqual(result[2][0], 18.608, 2)
        self.assertAlmostEqual(result[3][0], 8.928, 2)

    def test_sadeghi(self):
        '''
        Values checked at https://www.weather.gov/epz/wxcalc_rh
        For an independent result
        '''
        temp = numpy.ones((4, 1))
        tdew = numpy.ones((4, 1))
        z = numpy.ones((4, 1))

        temp[0][0] = 20.0
        tdew[0][0] = 20.0
        z[0][0] = 0

        temp[1][0] = 20.0
        tdew[1][0] = 10.0
        z[1][0] = 630

        temp[2][0] = 3.0
        tdew[2][0] = 1.0
        z[2][0] = 1500

        temp[3][0] = 20
        tdew[3][0] = 3.0
        z[3][0] = 3000

        result = get_tw_sadeghi(temp, tdew, z)

        self.assertEqual(result.shape[0], temp.shape[0])
        self.assertEqual(result.shape[1], temp.shape[1])

        self.assertAlmostEqual(result[0][0], 20.0, delta=0.1)
        self.assertAlmostEqual(result[1][0], 14.0, delta=0.2)
        self.assertAlmostEqual(result[2][0], 2.0, delta=0.1)
        self.assertAlmostEqual(result[3][0], 10.0, delta=0.2)


if __name__ == '__main__':
    unittest.main()
