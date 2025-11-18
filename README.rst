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
