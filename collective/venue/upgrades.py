# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging


logger = logging.getLogger('collective.venue upgrade')
PROFILE_ID = 'profile-collective.venue:base'


def unregister_resource(registry, resource):
    if registry and registry.getResource(resource):
        registry.unregisterResource(resource)
        logger.info("Removed {0} from {1}".format(resource, registry.id))


def upgrade_registry(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def upgrade_3_to_4(context):
    """Remove JS and CSS resources from portal_css and portal_js registry.
    Import resource registry configuration.
    """

    # Unregister JavaScript
    unregister_resource(
        getToolByName(context, 'portal_javascripts'),
        '++resource++collective.venue/scripts.js'
    )

    # Unregister CSS
    unregister_resource(
        getToolByName(context, 'portal_css'),
        '++resource++collective.venue/styles.css'
    )

    upgrade_registry(context)
