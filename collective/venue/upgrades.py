# -*- coding: utf-8 -*-
from collective.venue.behaviors import ILocation
from collective.venue.behaviors import IOrganizer
from plone import api
from plone.app.uuid.utils import uuidToObject
from Products.CMFCore.utils import getToolByName
from z3c.relationfield import RelationValue
from z3c.relationfield.event import _setRelation
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

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
        '++resource++collective.venue/scripts.js',
    )

    # Unregister CSS
    unregister_resource(
        getToolByName(context, 'portal_css'),
        '++resource++collective.venue/styles.css',
    )

    upgrade_registry(context)


def upgrade_5_to_6(context):
    """
    move fields:
    - from location_uid to location_ref
    - from organizer_uid to organizer_ref
    """
    location_brains = api.content.find(
        object_provides=ILocation.__identifier__
    )
    organizer_brains = api.content.find(
        object_provides=IOrganizer.__identifier__
    )
    for brain in location_brains:
        fix_ref(
            brain=brain, old_field='location_uid', new_field='location_ref'
        )
    for brain in organizer_brains:
        fix_ref(
            brain=brain, old_field='organizer_uid', new_field='organizer_ref'
        )


def fix_ref(brain, old_field, new_field):
    item = brain.getObject()
    uid = getattr(item, old_field, '')
    if not uid:
        return
    ref_obj = uuidToObject(uid)
    delattr(item, old_field)
    if not ref_obj:
        return
    intids_tool = getUtility(IIntIds)
    to_id = intids_tool.getId(ref_obj)
    rel = RelationValue(to_id)
    setattr(item, new_field, rel)
    _setRelation(item, new_field, rel)
    logger.info(
        'Fix "{field}" for {url}'.format(
            field=new_field, url=item.absolute_url()
        )
    )
