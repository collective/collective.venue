Changelog
=========

4.0 (2019-06-06)
----------------

Breaking changes:

    - The following settings are now handled by ``plone.formwidget.geolocation`` and have changed their prefix to ``geolocation``. They need to be upgraded manually: ``collective.venue.default_map_layer``, ``collective.venue.google_api_key``, ``collective.venue.map_layers``, ``collective.venue.show_google_maps_link``.

    - Rename ``collective.venue.icalexporter.AAFICalendarEventComponent`` to  ``collective.venue.icalexporter.VenueICalendarEventComponent``.
      The ``AAF`` name was a leftover from a client project.
      [thet]

    - Event accessor is now registered with ILocation behavior.
      With this change we don't need to override p.a.event accessor anymore.
      [cekk]

New features:

    - Refactor maps settings and indexer -> moved to ``plone.app.formwidget``
      and ``collective.geolocationbehavior``
      [petschki, thet]

    - uninstall profiles
      [petschki]

    - Customize event_summary view and portlet event renderer to properly show location info.
      [cekk]

Bug fixes:

    - Make the registration of the ``@@locationsearch`` view dependend on the availability of ``geopy``.
      Fixes #15.
      [thet]

    - Controlpanel: Fix problem where always only default values were shown but no already stored values.
      [thet]

    - ical export: Fix contact getter if IOrganizer behavior is not enabled.
      [cekk]

    - Remove registry initialization in bundle.
      [cekk]


3.1.2 (2017-12-06)
------------------

- Prevent ``ILocation`` behavior not adaptable in ``VenueEventAccessor``.
  [thet]

- Add ``IICalendarEventComponent`` adapter to customize the ical export of ``location``, ``contact`` and ``geo`` properties.
  [thet]

- Only include the leaflet bundle where it is needed via ``add_bundle_on_request``.
  [thet]

- Adapt the ``contenttype-venue`` icon to recent changes in plonetheme.barceloneta 1.7.4.
  [thet]


3.1.1 (2017-04-04)
------------------

- Explicitly include necessary zcml dependencies to avoid having to explictly doing that in tests.
  plone.app.testing disables z3c.autoinclude.
  [thet]


3.1 (2017-02-28)
----------------

- Remove styles for latitude/longitude.
  They are too unspecific and make Leaflet's layer selection very ugly and unusable.
  [thet]

- Improve bundle registration and include an upgrade step.
  [thet]


3.0.3 (2017-02-24)
------------------

- Depend on z3c.unconfigure < 1.1 again.
  buildout.coredev ist still depending on 1.0.1.
  [thet]


3.0.2 (2017-01-25)
------------------

- Remove z3c.unconfigure version depenency.
  buildout.coredev 5.1 now depends on 1.1.
  [thet]


3.0.1 (2017-01-13)
------------------

- German locales update.
  [thet]


3.0 (2016-10-06)
----------------

Breaking changes:

- Put fields on own tab in order to reduce clutter on default tab.
  [jensens]

- Optional dependency on collective.geolocationbehavior.
  If you want to use geolocation support, depend on the [geolocation] extra and add the ``geolocatable`` behavior from ``collective.geolocationbehavior``.
  [agitator, thet]

- Removed support for Plone < 5.
  [agitator, thet]

New features:

- Show the address in the marker popup.
  [thet]

- Provide a ``@@venue_overlay`` view for map overlays.
  [thet]

- Provide a venue tile when ``plone.tiles`` is installed, which is basically like the venue view.
  [thet]

- Allow configuration of Google API key for searching geo coordinates, show link to Google maps, default map layer and available map layers.
  Upgrade step provided.
  [thet]

- Add a link to Google Maps.
  [thet]

- Add possibility to search the geo coordinates for an address.
  [thet]

- Re-arrange Venue forms and put map to top.
  [thet]

- Clean up behavior forms a bit.
  [thet]

- Update pot/po files + German translations.
  [jensens]

- Add behavior shortnames ``venue.locationreference`` and ``vanue.organizerreference``.
  [thet]

- Add ``IOrganizer`` behavior additional to the ``ILocation`` behavior.
  [thet]

- Upgraded profiles for Plone 5 resource registries.
  Added setuphandlers and upgrade steps.
  [agitator]

- Added social media fields behavior from c.address.
  [agitator]

- Moved out geolocation support to extras (WIP).
  [agitator]

- Disable not working registry and adapter entries.
  [agitator]

Bug fixes:

- Hide uninstall profile from site setup and quickinstaller.
  [thet]


2.1.3 (2016-02-04)
------------------

- Change all ``RichTextValue.output`` to ``RichTextValue.output_relative_to`` references for correct relative link resolving.
  Also see: https://github.com/plone/plone.app.textfield/pull/17
  [thet]


2.1.2 (2015-10-06)
------------------

- Let ``SearchBaseVocabulary`` only return ``Folder`` and ``Plone Site`` types
  instead of all folderish types to reduce the vocabulary list.
  [thet]

- Rename ``VenueVocabulary`` to ``SearchBaseVocabulary``. The old name was
  misleading.
  [thet]


2.1.1 (2015-10-02)
------------------

- Fix indexer, where notes were not properly extracted and indexer failed.
  [thet]


2.1 (2015-09-25)
----------------

- Allow to show venues via their uid from other subsites, which would otherwise
  be inaccessible e.g. in a virtual hosting environment.
  [thet]

- Add controlpanel with configure options for a venue search base folder and a
  default venue. The search base folder is useful in multi-site environments.
  [thet]

- Better SearchableText indexing.
  [thet]


2.0 (2015-07-15)
----------------

- Remove Leaflet code. It's now in plone.formwidget.geolocation.
  [thet]

- Remove the ``div.geolocation`` elements. Instead, render the list of
  geolocation points as JSON value on a ``data-geopoints`` attrbute on the map
  element.
  [thet]

- Include a IEventAccessor implentation for IDXEvent and override the default
  implementation from plone.app.event. This implementation's locaion property
  returns a HTML link to a location object, if defined.
  [thet]

- Remove ``geolocation_display.pt`` and ``geolocation_input.pt`` templates.
  Those were just overriding the id attribute from the original templates under
  ``plone.formwidget.geolocation``. We should use css classes anyways.
  [thet]

- Change the view name ``venue`` to ``venue_view`` to be more unique among
  content being traversed and also named venue.
  [thet]

- Remove Archetypes code. Since 2.0, we're only supporting Dexterity types
  based on plone.app.event >= 2.0.
  [thet]


1.1 (2014-07-04)
----------------

- Fix prepOverlay availability check, which has somehow changed to be only
  available on jQuery objects and not jQuery itself.
  [thet]

- JSLint'ing.
  [thet]

- Also support IEventAccessor in get_location and fix location not beeing
  displayed on ``@@event_listing`` views.
  [thet]

1.0 (2014-04-30)
----------------

- initial.
