collective.venue
================

This package provides an Dexterity content type for Venue with `geolocation <https://en.wikipedia.org/wiki/Geolocation>`_ support
for use with events or any other location specific content.


Features
========

Event Venue Settings Control panel.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/venue_controlpanel.png
    :align: center
    :height: 509px
    :width: 800px
    :alt: The Event Venue Settings control panel

    The Event Venue Settings control panel.

Event location `behavior <https://6.docs.plone.org/backend/behaviors.html>`_ called `collective.venue.default_venue`.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/ilocation_behavior.png
    :align: center
    :height: 41px
    :width: 852px
    :alt: The Event location Behavior

    The ``Event location`` Behavior.

Event organizer `behavior <https://6.docs.plone.org/backend/behaviors.html>`_ called `collective.venue.default_organizer`.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/iorganizer_behavior.png
    :align: center
    :height: 45px
    :width: 852px
    :alt: The Event organizer Behavior

    The ``Event organizer`` Behavior.

Venue Display `Tile <https://pypi.org/project/plone.tiles/>`_ for Plone Classic UI.


Translations
============

This product has been translated into:

- German
- Italian
- Spanish


Installation
============

If you installed Plone with `Cookieplone`_, you can install ``collective.venue`` add-on
from a source control system such as GitHub.

Add a line with ``collective.venue`` in the ``backend/requirements.txt`` file.

::

    collective.venue

Next add the add-on to ``zcml_package_includes`` in the file ``backend/instance.yaml`` so
that its configuration will load.

::

    default_context:
        zcml_package_includes: project_title, collective.venue

Finally, add the package's source to the ``mx.ini`` file.

::

    [collective.venue]
    url = https://github.com/collective/collective.venue.git
    pushurl = git@github.com:collective/collective.venue.git
    branch = master

To actually download and install the new add-on, run the following command.

::

    make backend-build

Now restart the backend.

----

If you installed Plone with `buildout`_, you can install ``collective.venue`` add-on
by adding it to your ``buildout`` eggs list like so:

::

    [buildout]

    ...

    eggs =
        collective.venue


and then running ``bin/buildout``

Now restart the instance.


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

.. _Cookieplone: https://github.com/plone/cookieplone
.. _buildout: https://6.docs.plone.org/admin-guide/add-ons.html#buildout
