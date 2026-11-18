from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import logging


logger = logging.getLogger("collective.venue upgrade")
PROFILE_ID = "profile-collective.venue:base"


def unregister_resource(registry, resource):
    if registry and registry.getResource(resource):
        registry.unregisterResource(resource)
        logger.info(f"Removed {resource} from {registry.id}")


def upgrade_registry(context):
    setup = getToolByName(context, "portal_setup")
    setup.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")


def upgrade_3_to_4(context):
    """Remove JS and CSS resources from portal_css and portal_js registry.
    Import resource registry configuration.
    """

    # Unregister JavaScript
    unregister_resource(
        getToolByName(context, "portal_javascripts"),
        "++resource++collective.venue/scripts.js",
    )

    # Unregister CSS
    unregister_resource(
        getToolByName(context, "portal_css"), "++resource++collective.venue/styles.css"
    )

    upgrade_registry(context)


def upgrade_5_to_6(context):
    """Replace the Plone 5 resources with the webpack bundle.

    Remove the RequireJS resource definitions and the old bundle records,
    which contain obsolete settings like ``resources`` and
    ``stub_js_modules``. Then re-import the registry to register the new
    bundle and the content type icon.
    """
    registry = getUtility(IRegistry)
    prefixes = (
        "plone.resources/collective-venue.",
        "plone.resources/collective-venue-bundle.",
        "plone.bundles/collective-venue-bundle.",
    )
    for key in [it for it in registry.records if it.startswith(prefixes)]:
        del registry.records[key]
        logger.info(f"Removed registry record {key}")

    upgrade_registry(context)
