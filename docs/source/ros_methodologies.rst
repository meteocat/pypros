Rain or Snow
============

Knowledge of surface precipitation type can be critical during
snow events at low altitudes or in regions not used to this phenomena.
For this purpose, previous studies developed several methodologies to 
discriminate precipitation types using meteorological surface observations.
Some of them are implemented in this package.

There are different approaches to address this issue:

   - Static threshold
   - Linear transition
   - Sigmoidal curves

Static threshold
----------------

A single temperature value is set as a threshold from which precipitation
type is discriminated. If temperature is above the threshold, precipitation
is classified as rain, otherwise as snow.

Wet bulb temperature
~~~~~~~~~~~~~~~~~~~~

#TODO Wet bulb temperature threshold is implemented in this package.

National Mosaic and Multi-Sensor QPE System (NMQ)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A complete precipitation classification process is defined in the NMQ system (Zhang et al. 2011). However,
a reduced version of it is considered in this study. If surface temperature is less than 2°C and wet bulb temperature
less than 0°C, precipitation is in form of snow. Otherwise, the NMQ procedure classifies precipitation as hail, warm
rain, stratiform rain or convective rain. However, in this study, distinct types of rain are not taken into account and
precipitation not categorized as snow is labelled as rain.


#TODO other static threshold

Linear transition
-----------------

#TODO

Sigmoidal curves
----------------

Koistinen and Saltikoff (KS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The methodology proposed by Koistinen and Saltikoff (1998) provides an 
empirical formula to calculate the probability of precipitation type using
temperature and relative humidity observations. Formally, the formula
calculates the probability of rain and two thresholds are set to discriminate
between snow, sleet and rain. In our case, the equation is flipped, so 
probability of snow is determined by (1) which may be expressed as

.. math::
    p(snow) = 1 - \dfrac{1}{1 + e^{22 - 2.7\cdot T - 0.2 \cdot RH}}

where T corresponds to temperature in Celsius and RH to relative humidity in %. If p(snow) obtained values are
below 0.33 precipitation is in form of rain, if they are between 0.33 and 0.66 in form of sleet and classified as snow
if they are above 0.66.

Liu S-shape curve (LiuS)
~~~~~~~~~~~~~~~~~~~~~~~~

#TODO
