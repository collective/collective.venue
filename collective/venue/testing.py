# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.venue


class CollectiveVenueLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.venue)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.venue:default')


COLLECTIVE_VENUE_FIXTURE = CollectiveVenueLayer()


COLLECTIVE_VENUE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_VENUE_FIXTURE,),
    name='CollectiveVenueLayer:IntegrationTesting',
)


COLLECTIVE_VENUE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_VENUE_FIXTURE,),
    name='CollectiveVenueLayer:FunctionalTesting',
)


COLLECTIVE_VENUE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_VENUE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveVenueLayer:AcceptanceTesting',
)
