<div align="center">
    <h1 align="center">collective.venue</h1>
</div>
<div align="center">
[![PyPI](https://img.shields.io/pypi/v/collective.venue)](https://pypi.org/project/collective.venue/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.venue)](https://pypi.org/project/collective.venue/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.venue)](https://pypi.org/project/collective.venue/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.venue)](https://pypi.org/project/collective.venue/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.venue)](https://pypi.org/project/collective.venue/)

[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.venue)](https://pypi.org/project/collective.venue/)

[![CI](https://github.com/collective/collective.venue/actions/workflows/main.yml/badge.svg)](https://github.com/collective/collective.venue/actions/workflows/main.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.venue)](https://github.com/collective/collective.venue)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.venue?style=social)](https://github.com/collective/collective.venue)

</div>

Reference venue objects from events. Optionally with geolocation support.

## Features

This package provides an Dexterity content type for Venue with `geolocation <https://en.wikipedia.org/wiki/Geolocation>`\_ support
for use with events or any other location specific content.

Event Venue Settings Control panel.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/venue_controlpanel.png
:align: center
:height: 509px
:width: 800px
:alt: The 'Event Venue Settings' control panel

    The ``Event Venue Settings`` control panel.

---

Event location `behavior <https://6.docs.plone.org/backend/behaviors.html>`\_ called `collective.venue.default_venue`.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/ilocation_behavior.png
:align: center
:height: 41px
:width: 852px
:alt: The 'Event location' Behavior

    The ``Event location`` Behavior.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/ilocation_behavior_used.png
:align: center
:height: 321px
:width: 800px
:alt: Using the 'Event location' Behavior into the Document content type

    Using the ``Event location`` Behavior into the Document content type.

---

Event organizer `behavior <https://6.docs.plone.org/backend/behaviors.html>`\_ called `collective.venue.default_organizer`.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/iorganizer_behavior.png
:align: center
:height: 45px
:width: 852px
:alt: The 'Event organizer' Behavior

    The ``Event organizer`` Behavior.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/iorganizer_behavior_used.png
:align: center
:height: 316px
:width: 800px
:alt: Using the 'Event organizer' Behavior into the Document content type

    Using the ``Event organizer`` Behavior into the Document content type.

---

Dexterity content type called `Venue` with geolocation support.

.. figure:: https://raw.githubusercontent.com/collective/collective.venue/refs/heads/master/docs/images/venue_content_type.png
:align: center
:height: 1438px
:width: 800px
:alt: Dexterity content type called 'Venue' with geolocation support

    Dexterity content type called ``Venue`` with geolocation support.

---

Venue Display `Tile <https://pypi.org/project/plone.tiles/>`\_ for Plone Classic UI.

## Installation

Install collective.venue with `pip`:

```shell
pip install collective.venue
```

And to create the Plone site:

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/collective/collective.venue/issues)
- [Source code](https://github.com/collective/collective.venue/)

### Prerequisites ✅

- An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
- [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
- [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
- [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
- [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.venue.git
    cd collective.venue
    ```

2.  Install this code base.

    ```shell
    make install
    ```

## License

The project is licensed under GPLv2.
