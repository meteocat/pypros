
Linear transition
=================

Two threshold values are set to discriminate precipitation type between
rain (:math:`th_{rain}`) and snow (:math:`th_{snow}`). It can be either
used with any meteorological field, but with thresholds properly
defined. If a value of the meteorological field is above
:math:`th_{rain}`, precipitation is classified as rain. On the other
hand, if the values is below :math:`th_{snow}`, precipitation is
classified as snow. A linear transition is assumed for values between
:math:`th_{snow}` and :math:`th_{rain}`, then precipitation is
classified as a mixed type.

If the meteorological field chosen to discriminate air is air
temperature:

:math:`\begin{equation*}
T_{a} <= T_{snow} \longrightarrow Snow \\
T_{snow} < T_{a} < T_{rain} \longrightarrow Mixed \\
T_{a} >= T_{rain} \longrightarrow Rain
\end{equation*}`

In the following example we’ll show how PyPROS classifies precipitation
considering the linear transition methodology.

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

Air temperature transition
~~~~~~~~~~~~~~~~~~~~~~~~~~

Since we want to apply an air temperature linear transition, first we’ll
define ``method`` PyPros parameter as ``'linear_tr'`` and then we’ll set
the ``threshold`` parameter to [0, 3] (:math:`^{\circ}`\ C).

.. code:: ipython3

    method = 'linear_tr'
    threshold = [0, 3]

Now, we’re ready to call PyPros class!

.. code:: ipython3

    linear_tr = PyPros(variables_files, method, threshold, data_format)

We can get a quicklook of the obtained field using ``plot_pros``
function:

.. code:: ipython3

    import matplotlib.pyplot as plt
    plt.imshow(linear_tr.result)
    plt.show()

In addition, we can save the precipitation type field in a raster file
using ``save_file`` function:

.. code:: ipython3

    linear_tr.save_file(linear_tr.result, '../sample-data/output/linear_tr.tif')

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

    linear_tr_masked = linear_tr.refl_mask(refl_array)
    
    linear_tr.save_file(linear_tr_masked, '../sample-data/output/linear_tr_masked.tif')
