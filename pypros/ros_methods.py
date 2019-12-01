"""Implements several rain or snow methodologies.
"""
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


def calculate_single_threshold(field, th):
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


def calculate_dual_threshold(field, th_s, th_r):
    """Calculates the precipitation type based on two threshold
    values, one for rain and one for snow.
    If value >= th_r --> rain --> 0
    If value <= th_s --> snow --> 1
    If th_s < value < th_r --> mixed --> 0.5

    Args:
        field (float, numpy array): Meteorological variable field
        th_s (float): Snow threshold. Values below this threshold
                      classified as snow.
        th_r (float): Rain threshold. Values above this threshold
                      classified as rain.

    Raises:
        ValueError: Raised if th_r is smaller than th_s.

    Returns:
        float, numpy array: Precipitation type field
    """
    if th_r <= th_s:
        raise ValueError("Incorrect thresholds, th_s value must be " +
                         "smaller than th_r")

    above_th_r = where(field >= th_r)
    under_th_s = where(field <= th_s)
    mixed = where((field < th_r) & (field > th_s))

    field[above_th_r] = 0
    field[under_th_s] = 1
    field[mixed] = 0.5

    return field


def calculate_linear_transition(field, th_s, th_r):
    """Calculates the probability of precipitation type based on
    two threshold values, one for rain and one for snow. Assumes
    a linear transition between them.
    If value >= th_r --> rain --> 0
    If value <= th_s --> snow --> 1
    If th_s < value < th_r --> mixed --> (0, 1)

    Args:
        field (float, numpy array): Meteorological variable field
        th_s (float): Snow threshold. Values below this threshold
                      classified as snow.
        th_r (float): Rain threshold. Values above this threshold
                      classified as rain.

    Raises:
        ValueError: Raised if th_r is smaller than th_s.

    Returns:
        float, numpy array: Probability of precipitation type field
    """
    if th_r <= th_s:
        raise ValueError("Incorrect thresholds, th_s value must be " +
                         "smaller than th_r")

    above_th_r = where(field >= th_r)
    under_th_s = where(field <= th_s)
    mixed = where((field < th_r) & (field > th_s))

    field[above_th_r] = 0
    field[under_th_s] = 1
    field[mixed] = (field[mixed] - th_r) / (th_s - th_r)

    return field
