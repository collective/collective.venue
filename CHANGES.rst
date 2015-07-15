Changelog
=========

2.0 (unreleased)
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
