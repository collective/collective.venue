collective.venue
================

This package provides an Dexterity Venue type for use with events or any other
purpose.

.. note::

    This is the Dexterity only branch for use with plone.app.event >=
    2.0. If you want to use collective.venue together with Archetypes
    based plone.app.event < 2.0 types, use the 1.x branch.


Geolocation
===========

If you want to use collective.venue with geolocation behavior, you should add the following line to your eggs buildout section:

    eggs =
        plone.app.multilingual[archetypes]


.. note::

    Full geolocation support on Plone 5 is still in progress
