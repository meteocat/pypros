'''Functions to calculate the probability of rain or snow.
For a point or numpy arrays
'''
from pypros.dewpoint import td2hr
import numpy


def calculate_koistinen_saltikoff(temp, tempd):
    """Returns the Koistinen-Saltikoff value.

    Koistinen J., Saltikoff E. (1998): Experience of customer products of
    accumulated snow, sleet and rain,
    COST 75 Final Seminar on Advanced Weather Radar Systems, Locarno,
    Switzerland. EUR 18567 EN, 397-406.

    The formula values are

    - prob < 0.3 --> rain
    - 0.3 < prob < 0.7 --> sleet
    - prob > 0.7 --> snow

    Both float values or numpy matrices can be passed as input
    and get as output

    Args:
        temp (float, numpy array): The temperature in Celsius
        tempd (float, numpy array): The dew point in Celsius

    Returns:
        float, numpy array: The Koistinen J., Saltikoff E. formula value
    """
    prob = 1 - 1 / (1 + 2.7182818 ** (22.0-2.7*temp-0.2*td2hr(temp, tempd)))
    return prob


def calculate_pros(temp, tempd, refl, method='ks'):
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
                                tw for the wet bulb method

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

    if method == 'ks':
        prob_bins = numpy.array([0.0, 0.3, 0.7])
        refl_bins = numpy.array([1, 5, 10, 15, 25])

        prob = calculate_koistinen_saltikoff(temp, tempd)

        ks_class = numpy.digitize(prob, prob_bins) - 1
        refl_class = numpy.digitize(refl, refl_bins)

        pros = (refl_class + ks_class * 5) * (refl >= 1)
    else:
        raise ValueError("Non valid method. Valid values are ks and tw")

    return pros
