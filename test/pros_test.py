import unittest
import numpy
from osgeo import gdal, osr
from pypros.pros import PyPros


class TestCalculateRos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_format = {'vars_files': ['tair', 'tdew', 'refl']}
        cls.variables_file = ['/tmp/tair.tif',
                              '/tmp/tdew.tif',
                              '/tmp/refl.tif']
        size = [3, 3]
        tair = numpy.ones(size)
        tdew = numpy.ones(size)
        refl = numpy.ones(size)

        refl_values = [0.2, 2, 6, 12, 16, 26]
        for i in range(3):
            tair[0][i] = 20
            tdew[0][i] = 20
            tair[1][i] = 2
            tdew[1][i] = 0
            tair[2][i] = -1
            tdew[2][i] = -1
            refl[0][i] = refl_values[i]
            refl[1][i] = refl_values[i]
            refl[2][i] = refl_values[i]

        fields = [tair, tdew, refl]

        for i in range(len(fields)):
            driver = gdal.GetDriverByName('GTiff')
            d_s = driver.Create(cls.variables_file[i], size[1], size[0], 1,
                                gdal.GDT_Float32)

            d_s.GetRasterBand(1).WriteArray(fields[i])
            d_s.SetGeoTransform((0, 100, 0, 200, 0, -100))

            proj = osr.SpatialReference()
            proj.ImportFromEPSG(25831)

            d_s.SetProjection(proj.ExportToWkt())

            d_s = None

        cls.method = 'ks'

    def test_init(self):
        inst = PyPros(self.variables_file, self.method, self.data_format)
        self.assertEqual(inst.result.shape, (3, 3))

        inst.save_file(inst.result, "/tmp/out.tiff")

    def test_init_different_methods(self):
        inst = PyPros(self.variables_file, 'ks', self.data_format)
        self.assertEqual(inst.result.shape, (3, 3))

        inst = PyPros(self.variables_file, 'static_tw', self.data_format)
        self.assertEqual(inst.result.shape, (3, 3))

        inst = PyPros(self.variables_file, 'static_ta', self.data_format)
        self.assertEqual(inst.result.shape, (3, 3))

        inst = PyPros(self.variables_file, 'linear_tr', self.data_format)
        self.assertEqual(inst.result.shape, (3, 3))

    def test_refl_mask(self):
        inst = PyPros(self.variables_file, 'ks', self.data_format)
        pros_masked = inst.refl_mask()

        # rain
        for i in range(1, 3):
            self.assertEqual(pros_masked[0][i], i)
        # sleet
        for i in range(1, 3):
            self.assertEqual(pros_masked[1][i], 5 + i)
        # snow
        for i in range(1, 3):
            self.assertEqual(pros_masked[2][i], 10 + i)

        inst = PyPros(self.variables_file, 'static_tw', self.data_format)
        pros_masked = inst.refl_mask()

        # rain
        for i in range(1, 3):
            self.assertEqual(pros_masked[0][i], i)
        # snow
        for i in range(1, 3):
            self.assertEqual(pros_masked[2][i], 10 + i)

        inst = PyPros(self.variables_file, 'static_ta', self.data_format)
        pros_masked = inst.refl_mask()

        # rain
        for i in range(1, 3):
            self.assertEqual(pros_masked[0][i], i)
        # snow
        for i in range(1, 3):
            self.assertEqual(pros_masked[2][i], 10 + i)

        inst = PyPros(self.variables_file, 'linear_tr', self.data_format)
        pros_masked = inst.refl_mask()

        # rain
        for i in range(1, 3):
            self.assertEqual(pros_masked[0][i], i)
        # sleet
        for i in range(1, 3):
            self.assertEqual(pros_masked[1][i], 5 + i)
        # snow
        for i in range(1, 3):
            self.assertEqual(pros_masked[2][i], 10 + i)


if __name__ == '__main__':
    unittest.main()
