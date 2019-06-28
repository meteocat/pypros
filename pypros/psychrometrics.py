'''
Psychrometric calculations
'''
from numpy import power
from numpy import arctan
from numpy import array
from math import exp


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
    """Gets the wet bulb temperature from the temperature and the dew point
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


def trhp2tw(temp, rh, z):
    """Gets the wet bulb temperature from the temperature, relative humidity
    and pressure. Formula taken from:
    https://www.weather.gov/epz/wxcalc_wetbulb (Brice and Hall, 2003)

    Args:
        temp (float, numpy array): The temperature in Celsius
        rh (float, numpy array): The relative humidity in [0,1]
        z (float, numpy array): The altitude in metres

    Returns:
        float, numpy array: The wet bulb temperature in Celsius
    """
    shape = temp.shape

    temp = temp.reshape(-1)
    rh = rh.reshape(-1)
    p = _get_p_from_z(z).reshape(-1)

    tw_out = []

    for i in range(len(temp)):
        rh_s = rh[i] + 1
        tw = temp[i]

        while rh_s >= rh[i]:
            tw = tw - 0.001
            es = 6.112*exp(17.67*temp[i]/(temp[i]+243.5))
            ew = 6.112*exp(17.67*tw/(tw+243.5))
            e = ew - p[i]*(temp[i]-tw)*0.00066*(1+(0.00115*tw))

            rh_s = e / es * 100

        tw_out.append(tw)

    tw_out = array(tw_out)
    tw_out = tw_out.reshape(shape)

    return tw_out


def _get_p_from_z(z):
    """Gets pressure field from altitude field considering an OACI atmosphere.

    Args:
        z (float, numpy array): The altitude in metres

    Returns:
        p: The pressure field in hPa
    """

    p = 1013.25 * (1 - 0.0065 * z / (15 + 0.0065 * z + 273.15)) ** 5.257

    return p


def get_tw_sadeghi(tair, tdew, z):
    '''Gets the wet bulb temperature from air temperature, dew point
    temperature and pressure. Formula taken from:
    https://journals.ametsoc.org/doi/pdf/10.1175/JTECH-D-12-00191.1

    Results close to trhp2tw, but computationally efficient

    Args:
        tair (float, numpy array): The air temperature in Celsius
        tdew (float, numpy array): The dew point temperature in Celsius
        z (float, numpy array): The altitude in metres

    Returns:
        float, numpy array: The wet bulb temperature in Celsius
    '''

    p = _get_p_from_z(z) / 10
    ea = 0.611*(10**(7.5*tdew/(237.3+tdew)))

    psych_ct = 6.42e-4

    lambda0 = 0.0014 * 2.71828**(0.027 * tair)
    xi = -3*(10**-7)*tair**3 - (10**-5)*tair**2 + 2*(10**-5)*tair + (
         4.44*(10**-2))
    phi = xi + psych_ct*p
    psi = 0.611 - psych_ct*p*(tair) - ea

    return (-phi + (phi**2 - 4*lambda0*psi)**(0.5)) / (2*lambda0)
