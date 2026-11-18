from collective.venue import upgrades
from plone.base.interfaces.resources import IBundleRegistry
from plone.base.interfaces.resources import IResourceRegistry
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import pytest


BUNDLE = "plone.bundles/collective-venue-bundle"


@pytest.fixture
def registry(portal):
    return getUtility(IRegistry)


class TestResources:
    def test_bundle_registered(self, registry):
        bundle = registry.forInterface(IBundleRegistry, prefix=BUNDLE)
        assert bundle.enabled is True
        assert bundle.depends == "plone"
        assert bundle.jscompilation == (
            "++plone++collective.venue/collective-venue-bundle/remote.min.js"
        )
        assert bundle.csscompilation == (
            "++plone++collective.venue/collective-venue.css"
        )

    def test_no_requirejs_resources(self, registry):
        assert not [
            key
            for key in registry.records
            if key.startswith("plone.resources/collective-venue")
        ]

    def test_contenttype_icon(self, registry):
        assert (
            registry["plone.icon.contenttype/venue"]
            == "++plone++bootstrap-icons/geo-alt.svg"
        )

    def test_static_resources(self, portal):
        for path in (
            "++plone++collective.venue/collective-venue.css",
            "++plone++collective.venue/collective-venue-bundle/remote.min.js",
        ):
            assert portal.restrictedTraverse(path) is not None


class TestUpgrade5to6:
    def test_upgrade_replaces_plone5_resources(self, portal, registry):
        # Simulate the Plone 5 registration.
        registry.registerInterface(
            IResourceRegistry, prefix="plone.resources/collective-venue"
        )
        registry["plone.resources/collective-venue.js"] = (
            "++plone++collective.venue/locationsearch.js"
        )
        registry[f"{BUNDLE}.jscompilation"] = (
            "++plone++collective.venue/collective-venue-bundle-compiled.js"
        )
        registry[f"{BUNDLE}.stub_js_modules"] = ["jquery", "pat-base"]
        del registry.records["plone.icon.contenttype/venue"]

        upgrades.upgrade_5_to_6(portal)

        assert not [
            key
            for key in registry.records
            if key.startswith("plone.resources/collective-venue")
        ]
        bundle = registry.forInterface(IBundleRegistry, prefix=BUNDLE)
        assert bundle.jscompilation == (
            "++plone++collective.venue/collective-venue-bundle/remote.min.js"
        )
        assert bundle.stub_js_modules == []
        assert "plone.icon.contenttype/venue" in registry.records
