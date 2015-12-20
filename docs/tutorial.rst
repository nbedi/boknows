============
Tutorial
============


Command Line Interface
----------------------

The command line interface is extremely basic at the moment. It is only 
connected to the csv_dump function to write a stream of NCAA statistics to 
several CSV files.

To use default settings specified in the csv_dump documentation, simply run:

.. code:: bash

    boknows

The command line interface documentation specifies optional arguments.

Python Modules
---------------

Eventually, the boknows package will include modules to access NCAA statistics as 
Python objects. Right now, you will only be able to import the existing utility 
functions to dump NCAA data to CSV files.

.. code:: python

    from boknows import utils

    # dump NCAA stats to CSV files
    utils.csv_dump()
