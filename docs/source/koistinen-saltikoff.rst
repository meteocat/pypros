
Koistinen-Saltikoff
===================

The methodology proposed by Koistinen and Saltikoff (1998) provides an
empirical formula to calculate the probability of precipitation type
using temperature and relative humidity observations. Formally, the
formula calculates the probability of rain and two thresholds are set to
discriminate between snow, sleet and rain. In our case, the equation is
flipped, so probability of snow is determined by (1) which may be
expressed as

:math:`\begin{equation*}
p(snow) = 1 - \dfrac{1}{1 + e^{22 - 2.7\cdot T - 0.2\cdot RH}}
\end{equation*}`

where T corresponds to temperature in Celsius and RH to relative
humidity in %. If p(snow) obtained values are below 0.33 precipitation
is in form of rain, if they are between 0.33 and 0.66 in form of sleet
and classified as snow if they are above 0.66.

In the following example we’ll show how PyPROS classifies precipitation
considering the Koistinen-Saltikoff methodology.

First of all, we’ll import the required libraries.

.. code:: python

    from pypros.pros import PyPros

As an example, we’ll get the precipitation type classification from
different methodologies for Catalonia on 2017-03-25 00.30 UTC. For this
purpose we’ll use an air temperature, dew point temperature, digital
elevation model (DEM) and reflectivity fields.

Those fields can be found in notebooks/data directory and we’ll keep the
path for all of them:

.. code:: python

    tair_file = '../sample-data/INT_TAIR_20170325_0030.tif'
    tdew_file = '../sample-data/INT_TDEW_20170325_0030.tif'
    dem_file = '../sample-data/DEM_CAT.tif'

Now, we’ll define those parameters that PyPros class uses and are the
same whether the methodology changes or not. These parameters are:
``variables_files`` and ``data_format``. For more information on this
class, see `PyPros Class <pypros_class.ipynb>`__ notebook.

.. code:: python

    variables_files = [tair_file,
                       tdew_file,
                       dem_file]
    data_format = {'vars_files':['tair', 'tdew', 'dem']}

Since we want to apply the Koistinen-Saltikoff methodology, first we’ll
define ``method`` PyPros parameter as ``'ks'`` and then we’ll set the
``threshold`` parameter to ``None``.

.. code:: python

    method = 'ks'
    threshold = None

Now, we’re ready to call PyPros class!

.. code:: python

    ks = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: python

    import matplotlib.pyplot as plt
    plt.imshow(ks.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: python

    ks.save_file(ks.result, '../sample-data/output/ks.tif')

If we have a reflectivity field, we can also apply it as a mask by using
``refl_mask`` function and save it as a raster file. However, we’ll have
to read first the reflectivity field. For this purpose we need to import
gdal.

.. code:: python

    from osgeo import gdal

    refl_file = '../sample-data/CAPPI_XRAD_20170325_0030.tif'
    refl_array = gdal.Open(refl_file).ReadAsArray()

Once we’ve read the ``refl_field`` we can call the ``refl_mask``
function.

.. code:: python

    ks_masked = ks.refl_mask(refl_array)

    ks.save_file(ks_masked, '../sample-data/output/ks_masked.tif')
