'''
Dew point calculations
'''
from numpy import power
from numpy import arctan


def td2hr(temp, tempd):
    """
    Returns the relative humidity from the temperature and the dew point
    Formula from:
    https://www.aprweather.com/pages/calc.htm

    Both float values or numpy matrices can be passed as input
    and get as output

    Args:
        temp (float, numpy array): The temperature in Celsius
        tempd (float, numpy array): The dew point in Celsius

    Returns:
        float, numpy array: The relative humidity in %
    """
    es = 10**(7.5*tempd/(237.7+tempd))
    e = 10**(7.5*temp/(237.7+temp))

    return 100*(es/e)


def hr2td(temp, r_h):
    '''
    Returns the dew point from the relative humidity and the temperature
    Formula from:
    https://www.aprweather.com/pages/calc.htm

    Both float values or numpy matrices can be passed as input
    and get as output

    Args:
        temp (float, numpy array): The temperature in Celsius
        r_h (float, numpy array): The relative humidity in %

    Returns:
        float, numpy array: The dew point in Celsius
    '''
    return (temp - (14.55 + 0.114 * temp) *
            (1.0 - (0.01 * r_h)) -
            (((2.5 + 0.007 * temp) * (1 - (0.01 * r_h))) ** 3.0) -
            ((15.9 + 0.117 * temp) * (1 - (0.01 * r_h)) ** 14.0))


def ttd2tw(temp, tempd):
    """Gets the wet bulb temperature from the temperature and the dew point.
    Formula taken from:
    https://journals.ametsoc.org/doi/full/10.1175/JAMC-D-11-0143.1

    TODO: Take altitude in account (should change algorithm)

    Args:
        temp (float, numpy array): The temperature in Celsius
        tempd (float, numpy array): The dew point in Celsius

    Returns:
        float, numpy array: The wet bulb temperature in Celsius
    """
    rh = td2hr(temp, tempd)

    return (temp*arctan(0.151977 * power((rh + 8.313659), 0.5)) +
            arctan(temp+rh) - arctan(rh-1.676331) +
            0.00391838*power(rh, 1.5) *
            arctan(0.023101*rh) - 4.686035)
