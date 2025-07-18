collective.venue
================

This package provides an Dexterity content type for Venue with `geolocation <https://en.wikipedia.org/wiki/Geolocation>`_ support
for use with events or any other location specific content.


Features
========

- Event Venue Settings Control panel.
- Event location `behavior <https://6.docs.plone.org/backend/behaviors.html>`_ called `collective.venue.default_venue`.
- Event organizer `behavior <https://6.docs.plone.org/backend/behaviors.html>`_ called `collective.venue.default_organizer`.
- Venue Display `Tile <https://pypi.org/project/plone.tiles/>`_.


Translations
============

This product has been translated into:

- German
- Italian
- Spanish


Installation
============

If you want to use ``collective.venue`` with geolocation behavior, you
should add the following line to your ``eggs`` buildout section:

::

    eggs =
        collective.venue [geolocation]


and then running ``bin/buildout``.


Contribute
==========

- Issue Tracker: https://github.com/collective/collective.venue/issues
- Source Code: https://github.com/collective/collective.venue


Support
=======

If you are having issues, please let us know at our `issue tracker <https://github.com/collective/collective.venue/issues>`_.


License
=======

The project is licensed under the GPLv2.
