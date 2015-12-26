.. _web-api:

======================
Web API
======================

boknows uses Flask to serve NCAA statistics as a basic Web API. The api connects 
to the :func:`boknows.utils.get_ncaa_data` function to return stats and store 
data for rudimentary caching.

.. autoflask:: boknows.api:app
    :undoc-static:
