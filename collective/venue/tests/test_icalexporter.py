# -*- coding: utf-8 -*-
from collective.venue import icalexporter
from collective.venue.behaviors import ILocation
from zope.interface import implementer

import unittest


@implementer(ILocation)
class StubEvent(object):
    """Stands in for an Event that has the ``ILocation`` behavior enabled,
    referencing some venue by uid.
    """

    def __init__(self, location_uid):
        self.location_uid = location_uid
        self.location_notes = u''


class StubVenue(object):
    """Stands in for the Venue object a location_uid resolves to."""


class GeoPropertyTests(unittest.TestCase):
    """collective.venue ships a ``geolocation`` extra. Sites that don't
    install it (see the ``default-nogeolocation`` profile) still enable the
    ``ILocation`` behavior on events, since that part doesn't depend on
    geolocation at all.
    """

    def setUp(self):
        self.addCleanup(
            setattr, icalexporter, 'uuidToObject', icalexporter.uuidToObject
        )
        self.addCleanup(
            setattr, icalexporter, 'IGeolocatable', icalexporter.IGeolocatable
        )

    def _component(self, context):
        # Build the view without going through ICalendarEventComponent's
        # __init__, which adapts to IEventAccessor and would require a full
        # Plone site just to exercise this one property.
        component = icalexporter.VenueICalendarEventComponent.__new__(
            icalexporter.VenueICalendarEventComponent
        )
        component.context = context
        return component

    def test_geo_without_location(self):
        component = self._component(object())
        self.assertIsNone(component.geo)

    def test_geo_without_geolocationbehavior_installed(self):
        # collective.geolocationbehavior failed to import, so the module
        # level IGeolocatable is None, exactly as it is on a site that
        # didn't pull in the "geolocation" extra.
        icalexporter.IGeolocatable = None
        icalexporter.uuidToObject = lambda uid: StubVenue()
        component = self._component(StubEvent('a-venue-uid'))
        self.assertIsNone(component.geo)

    def test_geo_with_unresolvable_venue(self):
        icalexporter.uuidToObject = lambda uid: None
        component = self._component(StubEvent('missing-uid'))
        self.assertIsNone(component.geo)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
