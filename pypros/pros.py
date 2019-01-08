'''Functions to calculate the probability of rain or snow.
For a point or numpy arrays
'''
from pypros.psychrometrics import ttd2tw
from pypros.ros_methods import calculate_koistinen_saltikoff
from pypros.ros_methods import calculate_static_threshold
import numpy


def calculate_pros(temp, tempd, method='ks'):
    if not (type(temp) == type(tempd)):
        raise IndexError("The three parameters must have the same type")
    if type(temp) == numpy.ndarray and (temp.shape != tempd.shape):
        raise IndexError("The matrices must have the same dimensions")

    if method == 'ks':
        pros = calculate_koistinen_saltikoff(temp, tempd)
    elif method == 'tw':
        t_w = ttd2tw(temp, tempd)
        pros = calculate_static_threshold(t_w, 1.5)
    else:
        raise ValueError("Non valid method. Valid values are ks and tw")
    
    return pros


def calculate_pros_refl(temp, tempd, refl, method='ks'):
    """Calculates the probability of snow. The output classification is as follows:

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
        temp (float, numpy array): The temperature in Celsius
        tempd (float, numpy array): The dew point in Celsius
        refl (float, numpy array): The reflectivity, in dBZ
        method (str, optional): Defaults to 'ks'.
                                ks for the Koistinen-Saltikoff method,
                                tw for the wet bulb < 1.8 C method

    Raises:
        IndexError: Raised if the types don't match in size ot type
        ValueError: Raised when the method is not valid (ks or tw)

    Returns:
       float, numpy array: The probability of snow classification value
    """
    if not (type(temp) == type(tempd) == type(refl)):
        raise IndexError("The three parameters must have the same type")
    if type(temp) == numpy.ndarray and (
                                        temp.shape != tempd.shape or
                                        tempd.shape != refl.shape):
        raise IndexError("The matrices must have the same dimensions")

    refl_bins = numpy.array([1, 5, 10, 15, 25])
    refl_class = numpy.digitize(refl, refl_bins)

    if method == 'ks':
        prob_bins = numpy.array([0.0, 0.3, 0.7])
        prob = calculate_koistinen_saltikoff(temp, tempd)
        ks_class = numpy.digitize(prob, prob_bins) - 1
        pros = (refl_class + ks_class * 5) * (refl >= 1)

    elif method == 'tw':
        t_w = ttd2tw(temp, tempd)
        rain = 1 - numpy.digitize(t_w, numpy.array([1.8]))
        pros = (refl_class + rain * 10) * (refl >= 1)
    else:
        raise ValueError("Non valid method. Valid values are ks and tw")
    return pros
