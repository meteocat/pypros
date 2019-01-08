from pypros.psychrometrics import td2hr
from numpy import where


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


def calculate_static_threshold(field, th):
    """Calculates the precipitation type based on a threshold value.
    If value > threshold --> rain --> 0
    If value <= threshold --> snow --> 1

    Args:
        field (float, numpy array): Meteorological variable field
        th (float): Threshold from which precipitation type is discriminated

    Returns:
        float, numpy array: Precipitation type field
    """
    above_th = where(field > th)
    under_th = where(field <= th)

    field[above_th] = 0
    field[under_th] = 1

    return field
