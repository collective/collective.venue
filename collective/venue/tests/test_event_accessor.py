# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.venue.testing import (
    COLLECTIVE_VENUE_INTEGRATION_TESTING,
)  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.event.interfaces import IEventAccessor
from z3c.relationfield import RelationValue
from z3c.relationfield.event import _setRelation
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestEventAccessor(unittest.TestCase):
    """Test that collective.venue is properly installed."""

    layer = COLLECTIVE_VENUE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            'Event', 'test-event', title=u"Test event", location="Wonderland"
        )
        self.event = self.portal['test-event']

    def test_get_standard_location_if_location_ref_not_set(self):
        """Test if collective.venue is installed."""
        accessor = IEventAccessor(self.event)
        self.assertIn(self.event.location, accessor.location)

    def test_get_venue_location_if_location_ref_is_set(self):
        """Test if collective.venue is installed."""
        venue_id = self.portal.invokeFactory(
            'Venue', 'test-venue', title=u"Test Venue"
        )
        venue = self.portal[venue_id]

        intids_tool = getUtility(IIntIds)
        to_id = intids_tool.getId(venue)
        rel = RelationValue(to_id)
        self.event.location_ref = rel
        accessor = IEventAccessor(self.event)
        self.assertNotIn(self.event.location, accessor.location)
        self.assertIn(venue.title, accessor.location)
