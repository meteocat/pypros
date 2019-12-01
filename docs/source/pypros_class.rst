PyPros class
============

PyPros is the main class of this library as it implements the different
methodologies available to discriminate the surface precipitation type
using surface observations.

In this notebook we’ll cover the parameters of PyPros class and their
format depending on the rain or snow methodology.

First of all, we’ll import PyPros class.

.. code:: python

    from pypros.pros import PyPros

``PyPros`` class receives four parameters:

-  variables_files: A list of the files paths containing the fields of
   required variables
-  method: The surface precipitation type method to use
-  threshold: The value of the threshold(s) to be used by the chosen
   method
-  data_format: A dictionary containing the order of the fields in
   variables_files

Variables_files
^^^^^^^^^^^^^^^

There are two mandatory fields to include: air temperature and dew point
temperature. Both fields allow to use all the implemented methodologies
of surface precipitation type discrimination.

Digital Elevation Model (DEM) is an optional field which allows to
calculate accurately the wet bulb temperature (if this method is
selected) by using altitude values. Otherwise, wet bulb temperature is
derived from air and dew point temperature fields only.

First, we’ll define the paths to each field and we’ll set
``variables_file`` with all of them.

.. code:: python

    tair_file = '../sample-data/INT_TAIR_20170325_0030.tif'
    tdew_file = '../sample-data/INT_TDEW_20170325_0030.tif'
    dem_file = '../sample-data/DEM_CAT.tif'

    variables_files = [tair_file, tdew_file, dem_file]

Method and threshold
^^^^^^^^^^^^^^^^^^^^

The method is an optional parameter defaults to Koistinen and Saltikoff
method, which must be passed as ‘ks’. The following table illustrates
the different methodologies available, how they must be introduced in
``PyPros`` class and the kind of threshold required. If no threshold is
set, it assumes the default one.

+-----------------+-----------------+------------------+-----------------+
| Method          | Name            | Threshold        | Default         |
+=================+=================+==================+=================+
| Koistinen and   | ``'ks'``        | ``None``         | ``None``        |
| Saltikoff       |                 |                  |                 |
+-----------------+-----------------+------------------+-----------------+
| Air temperature | ``'static_ta'`` | ``float``        | ``0.0``         |
| static          |                 |                  |                 |
| threshold       |                 |                  |                 |
+-----------------+-----------------+------------------+-----------------+
| Wet bulb        | ``'static_tw'`` | ``float``        | ``1.5``         |
| temperature     |                 |                  |                 |
| static          |                 |                  |                 |
| threshold       |                 |                  |                 |
+-----------------+-----------------+------------------+-----------------+
| Air temperature | ``'linear_tr'`` | ``[th_l, th_u]`` | ``[0, 3]``      |
| linear          |                 |                  |                 |
| transition      |                 |                  |                 |
+-----------------+-----------------+------------------+-----------------+

Now, as an example, we’ll define wet bulb temperature static threshold
as the method to use and set threshold to 1.3\ :math:`^{\circ}`\ C.

.. code:: python

    method = 'static_tw'
    threshold = 1.3

Data format
~~~~~~~~~~~

This parameter is a dictionary containing a key, ``vars_files``
providing the order of the fields in ``variables_files``. The name of
the variables are the following ones:

+-------------------------+------------+
| Field                   | Name       |
+=========================+============+
| Air temperature         | ``'tair'`` |
+-------------------------+------------+
| Dew point temperature   | ``'tdew'`` |
+-------------------------+------------+
| Digital Elevation Model | ``'dem'``  |
+-------------------------+------------+

Then, we’ll set ``data_format`` parameter following the
``variables_files`` order:

.. code:: python

    data_format = {'vars_files': ['tair', 'tdew', 'dem']}

Now we’re ready to call PyPros class and obtain a surface
precipitation type field.

.. code:: python

    static_tw = PyPros(variables_files, method, threshold, data_format)

Once we’ve called the class, now we can obtain the surface precipitation
type field, apply the reflectivity mask available and save both in a
raster file.

To obtain the result, we must get the ``result`` attribute of the class.

.. code:: python

    static_tw_field = static_tw.result

And if we want to apply the reflectivity mask, we have to call
``refl_mask`` function from the PyPros class, which requires the
reflectivity field as a parameter. So before calling ``refl_mask``, we
have to prepare the reflectivity field.

First of all, as it’s a .tif file, we’ll import ``gdal`` library.

.. code:: python

    from osgeo import gdal
    refl_file = '../sample-data/CAPPI_XRAD_20170325_0030.tif'
    refl_array = gdal.Open(refl_file).ReadAsArray()

In this case we used gdal because we have the reflectivity field stored
in a .tif file, but for the ``refl_mask`` only an array is needed. So
any format can be used, as long as it is transformed into a numpy array.

.. code:: python

    static_tw_masked = static_tw.refl_mask(refl_array)

Now, we’ve obtained two fields that we can save in raster files using
``save_result`` function from PyPros class. This function receives two
parameters: the field matrix we want to save and the file path
destination.

.. code:: python

    static_tw.save_file(static_tw_field, '../sample-data/output/static_tw.tif')
    static_tw.save_file(static_tw_masked, '../sample-data/output/static_tw_masked.tif')

We can have a look at ``static_tw`` result by plotting it with imshow:

.. code:: python

    import matplotlib.pyplot as plt

    plt.imshow(static_tw.result)
    plt.colorbar()
    plt.show()

We have finished the introduction to PyPros class! Change the threshold values
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
and methods and see how the snow level varies!
''''''''''''''''''''''''''''''''''''''''''''''
