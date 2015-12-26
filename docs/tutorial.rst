============
Tutorial
============

Web API
--------

boknows uses Flask to serve NCAA statistics as a Web API. In the boknows folder, 
simply run 

.. code:: bash

    python boknows/api.py

to start the Flask app.

Reference the :ref:`web-api` documentation for endpoints.


Command Line Interface
----------------------

The command line interface is extremely basic at the moment. It is only 
connected to the csv_dump function to write a stream of NCAA statistics to 
a CSV file.

To use default settings specified in the csv_dump documentation, simply run:

.. code:: bash

    boknows

The :ref:`command-line-interface` documentation specifies optional arguments.
