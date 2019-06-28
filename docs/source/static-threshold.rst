
Static threshold
================

A single meteorological variable value is set as a threshold from which
precipitation type is discriminated. If the meteorological variable
value is above the threshold, precipitation is classified as rain,
otherwise as snow.

If air temperature (:math:`T_{a}`) is chosen as meteorological variable:

:math:`\begin{equation*}  
T_{a} <= T_{a_{threshold}} \longrightarrow Snow \\
T_{a} > T_{a_{threshold}} \longrightarrow Rain
\end{equation*}`

In the following example we’ll show how PyPROS classifies precipitation
considering the static threshold methodology.

First of all, we’ll import the required libraries.

.. code:: ipython3

    from pypros.pros import PyPros

As an example, we’ll get the precipitation type classification from
different methodologies for Catalonia on 2017-03-25 00.30 UTC. For this
purpose we’ll use an air temperature, dew point temperature, digital
elevation model (DEM) and reflectivity fields.

Those fields can be found in notebooks/data directory and we’ll keep the
path for all of them:

.. code:: ipython3

    tair_file = '../sample-data/INT_TAIR_20170325_0030.tif'
    tdew_file = '../sample-data/INT_TDEW_20170325_0030.tif'
    dem_file = '../sample-data/DEM_CAT.tif'


Now, we’ll define those parameters that PyPros class uses and are the
same whether the methodology changes or not. These parameters are:
``variables_files`` and ``data_format``. For more information on this
class, see `PyPros Class <pypros_class.ipynb>`__ notebook.

.. code:: ipython3

    variables_files = [tair_file,
                       tdew_file,
                       dem_file]
    data_format = {'vars_files':['tair', 'tdew', 'dem']}

Air temperature threshold
~~~~~~~~~~~~~~~~~~~~~~~~~

Since we want to apply a static air temperature threshold, first we’ll
define ``method`` PyPros parameter as ``'static_ta'`` and then we’ll set
the ``threshold`` parameter to 1.0\ :math:`^{\circ}`\ C.

.. code:: ipython3

    method = 'static_ta'
    threshold = 1.0

Now, we’re ready to call PyPros class!

.. code:: ipython3

    static_ta = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: ipython3

    import matplotlib.pyplot as plt
    plt.imshow(static_ta.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: ipython3

    static_ta.save_file(static_ta.result, '../sample-data/output/static_ta.tif')

If we have a reflectivity field, we can also apply it as a mask by using
``refl_mask`` function and save it as a raster file. However, we’ll have
to read first the reflectivity field. For this purpose we need to import
gdal.

.. code:: ipython3

    from osgeo import gdal
    
    refl_file = '../sample-data/CAPPI_XRAD_20170325_0030.tif'
    refl_array = gdal.Open(refl_file).ReadAsArray()

Once we’ve read the ``refl_field`` we can call the ``refl_mask``
function.

.. code:: ipython3

    static_ta_masked = static_ta.refl_mask()
    
    static_ta.save_file(static_ta_masked, '../sample-data/output/static_ta_masked.tif')

Wet bulb temperature threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want to apply a static wet bulb temperature threshold, so first we’ll
define ``method`` PyPros parameter as ``'static_tw'`` and then we’ll set
the ``threshold`` parameter to 1.5\ :math:`^{\circ}`\ C.

.. code:: ipython3

    method = 'static_tw'
    threshold = 1.5

Now, we’re ready to call PyPros class!

.. code:: ipython3

    static_tw = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: ipython3

    import matplotlib.pyplot as plt
    plt.imshow(static_tw.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: ipython3

    static_tw.save_file(static_tw.result, '../sample-data/output/static_tw.tif')

If we have a reflectivity field, we can also apply it as a mask by using
``refl_mask`` function and save it as a raster file. However, we’ll have
to read first the reflectivity field. For this purpose we need to import
gdal.

.. code:: ipython3

    from osgeo import gdal
    
    refl_file = '../sample-data/CAPPI_XRAD_20170325_0030.tif'
    refl_array = gdal.Open(refl_file).ReadAsArray()

Once we’ve read the ``refl_file`` we can call the ``refl_mask``
function.

.. code:: ipython3

    static_tw_masked = static_tw.refl_mask(refl_array)
    
    static_tw.save_file(static_tw_masked, '../sample-data/output/static_tw_masked.tif')
