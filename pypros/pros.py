'''Functions to calculate the precipitation type.
For a point or numpy arrays
'''
import numpy as np
import gdal
import osr
from pypros.psychrometrics import ttd2tw
from pypros.psychrometrics import get_tw_sadeghi
from pypros.ros_methods import calculate_koistinen_saltikoff
from pypros.ros_methods import calculate_single_threshold
from pypros.ros_methods import calculate_linear_transition
from pypros.ros_methods import calculate_dual_threshold


class PyPros:
    """
    Main project class. Discriminates precipitation type considering
    different methodologies using surface observations.
    """
    def __init__(self, variables_file, method='ks', threshold=None,
                 data_format=None):
        """
        Args:
            variables_file (str, list): The file paths containing air
                                        temperature, dew point
                                        temperature and (digital elevation
                                        model) fields.

            method (str): The precipitation type discrimination
                          method to use. Defaults to ks.

                          Available:
                            - ks       : Koistinen and Saltikoff method
                            - single_tw: A single wet bulb temperature
                                         threshold
                            - single_ta: A single air temperature threshold
                            - dual_tw  : A dual wet bulb temperature thresholds
                            - dual_ta  : A dual air temperature threshold
                            - linear_tr: Linear transition between rain
                                         and snow

            threshold (float, list): Threshold value(s) to use in the
                                     different methods available.

                                     Defaults to:
                                        - static_tw: 1.5
                                        - static_ta: 0.0
                                        - linear_tr: [0, 3]

            data_format (dict, optional): Defaults to None. The order of the
                                          variables in the variables files.
                                          Defaults to:
                                          {'vars_files': ['tair',
                                                          'tdew',
                                                          'dem']}

        Raises:
            ValueError: Raised when the method is not valid
        """
        if data_format is None:
            self.data_format = {'vars_files': ['tair', 'tdew', 'dem']}
        else:
            self.data_format = data_format

        if threshold is None:
            if method == 'static_ta':
                self.threshold = 0
            elif method == 'static_tw':
                self.threshold = 1.5
            elif method == 'linear_tr':
                self.threshold = [0, 3]
            elif method == 'ks':
                None
            else:
                raise ValueError('Non valid method. Valid values are ks and ' +
                                 'static_tw, static_ta and linear_tr')
        else:
            if method == 'single_ta' or method == 'single_tw':
                if not type(threshold) == float:
                    raise ValueError('The threshold for the method {} must ' +
                                     'be a float'.format(method))
            elif (method == 'linear_tr' or method == 'dual_ta'
                  or method == 'dual_tw'):
                if (not (type(threshold) == list or type(threshold) == tuple)
                   or len(threshold) != 2):
                    raise ValueError('The thresholds for the method {} must ' +
                                     'be a list/tuple of length ' +
                                     'two'.format(method))
            elif method == 'ks':
                None
            else:
                raise ValueError('Non valid method. Valid values are ks and ' +
                                 'single_tw, single_ta and linear_tr')

            self.threshold = threshold

        self.__read_variables_files__(variables_file)
        self.method = method

        tair = self.variables[self.data_format['vars_files'].index('tair')]
        tdew = self.variables[self.data_format['vars_files'].index('tdew')]

        if method == 'ks':
            self.result = calculate_koistinen_saltikoff(tair, tdew)
        elif method == 'single_tw' or method == 'dual_tw':
            try:
                dem = self.variables[
                      self.data_format['vars_files'].index('dem')]
            except ValueError:
                print('Since no DEM is supplied, wet bulb temperature ' +
                      'calculations will assume a constant pressure of ' +
                      '1013.25 hPa.')
                twet = ttd2tw(tair, tdew)
            else:
                twet = get_tw_sadeghi(tair, tdew, dem)
            if method == 'single_tw':
                self.result = calculate_single_threshold(twet, self.threshold)
            elif method == 'dual_tw':
                self.result = calculate_dual_threshold(twet, self.threshold[0],
                                                       self.threshold[1])
        elif method == 'single_ta':
            self.result = calculate_single_threshold(tair, self.threshold)
        elif method == 'linear_tr':
            self.result = calculate_linear_transition(tair, self.threshold[0],
                                                      self.threshold[1])
        elif method == 'dual_ta':
            self.result = calculate_dual_threshold(tair, self.threshold[0],
                                                   self.threshold[1])

    def __read_variables_files__(self, variables_file):
        if isinstance(variables_file, (list,)):
            self.variables = None
            for layer_file in variables_file:
                d_s = gdal.Open(layer_file)
                if d_s is None:
                    raise FileNotFoundError("[Errno 2] No such file or " +
                                            "directory: 'BadFile'")
                for i in range(d_s.RasterCount):
                    layer_data = d_s.GetRasterBand(i + 1)\
                                 .ReadAsArray()[np.newaxis, :, :]
                    if self.variables is None:
                        self.variables = layer_data
                    else:
                        try:
                            self.variables = np.concatenate((self.variables,
                                                             layer_data),
                                                            axis=0)
                        except Exception:
                            raise ValueError('Variables fields must have the' +
                                             ' same shape.')
        else:
            d_s = gdal.Open(variables_file)
            self.variables = d_s.ReadAsArray()

        self.out_proj = osr.SpatialReference()
        self.out_proj.ImportFromWkt(d_s.GetProjection())
        self.size = (d_s.RasterYSize, d_s.RasterXSize)
        self.geotransform = d_s.GetGeoTransform()
        d_s = None

    def save_file(self, field, file_name):
        """Saves the calculate field data into a file

        Args:
            file_name (str): The output file path
        """
        driver = gdal.GetDriverByName('GTiff')

        d_s = driver.Create(file_name, self.size[1], self.size[0], 1,
                            gdal.GDT_Float32)
        d_s.SetGeoTransform(self.geotransform)
        d_s.SetProjection(self.out_proj.ExportToWkt())

        d_s.GetRasterBand(1).WriteArray(field)

    def refl_mask(self, refl):
        """Calculates the precipitation type masked. The output classification
        is as follows:

        rain

        - 1dBZ : 1
        - 5dBZ: 2
        - 10dBZ : 3
        - 15dBZ: 4
        - 25dBZ : 5

        sleet

        - 1dBZ: 6
        - 5dBZ : 7
        - 10dBZ: 8
        - 15dBZ : 9
        - 25dBZ: 10

        snow

        - 1dBZ : 11
        - 5dBZ: 12
        - 10dBZ : 13
        - 15dBZ: 14
        - 25dbZ: 15

        Args:
            refl (numpy.array): Array with reflectivity values

        Raises:
            IndexError: Raised if the types don't match in size or type

        Returns:
            float, numpy array: The precipitation type classification value
        """
        if self.result.shape != refl.shape:
            raise IndexError('Variables fields must have the' +
                             ' same shape.')

        refl_bins = np.array([1, 5, 10, 15, 25])
        refl_class = np.digitize(refl, refl_bins)

        if self.method == 'ks' or self.method == 'linear_tr':
            prob_bins = np.array([0.0, 0.3, 0.7])
            ks_class = np.digitize(self.result, prob_bins) - 1
            pros = (refl_class + ks_class * 5) * (refl >= 1)

        elif self.method == 'single_tw' or self.method == 'single_ta':
            rain = np.digitize(self.result, np.array([1]))
            pros = (refl_class + rain * 10) * (refl >= 1)

        elif self.method == 'dual_tw' or self.method == 'dual_ta':
            prob_bins = np.array([0.0, 0.5, 1])
            dual_class = np.digitize(self.result, prob_bins) - 1
            pros = (refl_class + dual_class * 5) * (refl >= 1)

        return pros
