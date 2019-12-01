
pypros_run script
=================

If you want to run PyPros form terminal directly, you can use
``pypros_run`` script. Now we’ll how it must be called.

``pypros_run`` receives up to six arguments, since two of them are
optional. The arguments and their order are the following ones:

+-------+-------------+---------------------------------------+-----------+
| Order | Argument    | Description                           | Mandatory |
+=======+=============+=======================================+===========+
| 1     | tair        | Air temperature field file path       | ☑         |
+-------+-------------+---------------------------------------+-----------+
| 2     | tdew        | Dew point temperature field file path | ☑         |
+-------+-------------+---------------------------------------+-----------+
| 3     | config_file | Configuration file path               | ☑         |
+-------+-------------+---------------------------------------+-----------+
| 4     | out_file    | Digital Elevation Model file path     | ☑         |
+-------+-------------+---------------------------------------+-----------+
| 5     | dem         | Digital Elevation Model file path     | ☐         |
+-------+-------------+---------------------------------------+-----------+

The configuration file is a .json including the following parameters:

.. code:: json

       {
        "method": "single_tw",
        "threshold": 1.0,
        "data_format": {"vars_files": ["tair", "tdew", "dem"]},
        "refl_masked": "True"
       }

For more information about the pypros_run script configuration
parameters, see `PyPros Class <pypros_class.ipynb>`__.

In order to execute the script you must have pyPROS package installed,
see Documentation.

A configuration file and sample fields for air temperature, dew point
temperature, digital elevation model and radar reflectivity are
available in ``../sample-data/`` directory. We’ll introduce two examples
of how ``pypros_run`` script is run.

Air temperature single threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file must look like the following one. We’ll set the
threshold to 1.0\ :math:`^{\circ}`\ C.

.. code:: json

       {
        "method": "single_ta",
        "threshold": 1.0,
        "data_format": {"vars_files": ["tair", "tdew"]},
        "refl_masked": "False"
       }

Since we set ``refl_masked`` to ``False`` we do not have to import any
radar reflectivity field. We would execute the script this way:

.. code:: console

   > pypros_run [path to air temperature field] [path to dew point temperature field] [path to configuration file] [output path]

Wet bulb temperature threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file should include the following parameters. We’ll
set the threshold to 1.5\ :math:`^{\circ}`\ C.

.. code:: json

       {
        "method": "single_tw",
        "threshold": 1.5,
        "data_format": {"vars_files": ["tair", "tdew", "dem"]},
        "refl_masked": "True"
       }

Since we set ``refl_masked`` to ``True`` we have to include the radar
reflectivity field in the configuration file and as an script argument.
In addition, we have also included ``dem`` in order to take into account
altitude when calculating wet bulb temperature. We would execute the
script this way:

.. code:: console

   > pypros_run [path to air temperature field] [path to dew point temperature field] [path to configuration file] [output path] --dem [path to dem] --refl [path to radar reflectivity file]
