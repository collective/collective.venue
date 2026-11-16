from collective.venue import icalexporter
from collective.venue.behaviors import ILocation
from types import SimpleNamespace
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface

import pytest


class IStubGeolocatable(Interface):
    """Stands in for collective.geolocationbehavior's IGeolocatable."""


@implementer(ILocation)
class StubEvent:
    """An event with the ILocation behavior, referencing a venue by UID."""

    def __init__(self, location_uid):
        self.location_uid = location_uid
        self.location_notes = ""


class StubVenue:
    """The object a location UID resolves to."""

    def __init__(self, geolocation=None):
        self.geolocation = geolocation


def make_component(context):
    # Skip ICalendarEventComponent.__init__: it adapts to IEventAccessor,
    # which needs a Plone site, and the geo property does not use it.
    component = icalexporter.VenueICalendarEventComponent.__new__(
        icalexporter.VenueICalendarEventComponent
    )
    component.context = context
    return component


@pytest.fixture
def without_geolocationbehavior(monkeypatch):
    monkeypatch.setattr(icalexporter, "IGeolocatable", None)


@pytest.fixture
def with_geolocationbehavior(monkeypatch):
    monkeypatch.setattr(icalexporter, "IGeolocatable", IStubGeolocatable)


def resolve_to(monkeypatch, obj):
    monkeypatch.setattr(icalexporter, "uuidToObject", lambda uid: obj)


class TestGeoWithoutGeolocationbehavior:
    """Sites without the geolocation extra (profile default-nogeolocation)
    still reference venues from events through the ILocation behavior.
    """

    @pytest.fixture(autouse=True)
    def _setup(self, without_geolocationbehavior):
        pass

    def test_without_location(self):
        assert make_component(object()).geo is None

    def test_with_venue(self, monkeypatch):
        resolve_to(monkeypatch, StubVenue())
        assert make_component(StubEvent("a-venue-uid")).geo is None

    def test_with_unresolvable_venue(self, monkeypatch):
        resolve_to(monkeypatch, None)
        assert make_component(StubEvent("missing-uid")).geo is None


class TestGeoWithGeolocationbehavior:
    @pytest.fixture(autouse=True)
    def _setup(self, with_geolocationbehavior):
        pass

    def test_with_geolocated_venue(self, monkeypatch):
        venue = StubVenue(SimpleNamespace(latitude=47.27, longitude=11.39))
        alsoProvides(venue, IStubGeolocatable)
        resolve_to(monkeypatch, venue)
        assert make_component(StubEvent("a-venue-uid")).geo == {"value": (47.27, 11.39)}

    def test_with_venue_not_geolocatable(self, monkeypatch):
        resolve_to(monkeypatch, StubVenue())
        assert make_component(StubEvent("a-venue-uid")).geo is None

    def test_with_unresolvable_venue(self, monkeypatch):
        resolve_to(monkeypatch, None)
        assert make_component(StubEvent("missing-uid")).geo is None
