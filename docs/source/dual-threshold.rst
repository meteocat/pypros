Dual threshold
==============

Two threshold values are set to discriminate precipitation type between
rain (:math:`th_{rain}`) and snow (:math:`th_{snow}`). It can be either
used with any meteorological field, but with thresholds properly
defined. If a value of the meteorological field is above
:math:`th_{rain}`, precipitation is classified as rain. On the other
hand, if the value is below :math:`th_{snow}`, precipitation is
classified as snow. Finally, if values are between :math:`th_{snow}` and
:math:`th_{rain}`, precipitation is classified as a mixed type.

If the meteorological field chosen to discriminate precipitation is air
temperature:

:math:`\begin{equation*}
T_{a} <= T_{snow} \longrightarrow Snow \\
T_{snow} < T_{a} < T_{rain} \longrightarrow Mixed \\
T_{a} >= T_{rain} \longrightarrow Rain
\end{equation*}`

In the following example we’ll show how PyPROS classifies precipitation
considering the dual threshold scheme.

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

Air temperature thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~

Since we want to apply an air temperature dual threshold, first we’ll
define ``method`` PyPros parameter as ``'dual_ta'`` and then we’ll set
the ``threshold`` parameter to [0, 3] (:math:`^{\circ}`\ C).

.. code:: python

    method = 'dual_ta'
    threshold = [0, 3]

Now, we’re ready to call PyPros class!

.. code:: python

    dual_ta = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: python

    import matplotlib.pyplot as plt
    plt.imshow(dual_ta.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: python

    dual_ta.save_file(dual_ta.result, '../sample-data/output/dual_ta.tif')

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

    dual_ta_masked = dual_ta.refl_mask(refl_array)

    dual_ta.save_file(dual_ta_masked, '../sample-data/output/dual_ta_masked.tif')

Wet bulb temperature thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since we want to apply a wet bulb temperature dual threshold, first
we’ll define ``method`` PyPros parameter as ``'dual_tw'`` and then we’ll
set the ``threshold`` parameter to [0, 2] (:math:`^{\circ}`\ C).

.. code:: python

    method = 'dual_tw'
    threshold = [0, 2]

Now, we’re ready to call PyPros class!

.. code:: python

    dual_tw = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: python

    import matplotlib.pyplot as plt
    plt.imshow(dual_tw.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: python

    dual_tw.save_file(dual_tw.result, '../sample-data/output/dual_tw.tif')

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

    dual_tw_masked = dual_tw.refl_mask(refl_array)

    dual_tw.save_file(dual_tw_masked, '../sample-data/output/dual_tw_masked.tif')
