# -*- coding: utf-8 -*-
from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.behaviors import ILocation
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.uuid.utils import uuidToObject
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

import six


def _concat_and_utf8(*args):
    """Concats args with spaces between and returns utf-8 string, it does not
    matter if input was unicode or str.
    Taken from ``plone.app.contenttypes.indexers``
    """
    result = ''
    for value in args:
        if six.PY2 and isinstance(value, six.text_type):
            value = value.encode('utf-8', 'replace')
        if value:
            result = ' '.join((result, value))
    return result


# Index lat/lng of ILocation behavior providing objects like Events.
# IGeolocatable (which venue objects provide) are already indexed in
# collective.geolocationbehavior

@indexer(ILocation)
def latitude(obj):
    venue = uuidToObject(obj.location_uid)
    return venue.geolocation.latitude


@indexer(ILocation)
def longitude(obj):
    venue = uuidToObject(obj.location_uid)
    return venue.geolocation.longitude


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    meta_basic = IBasic(obj)
    venue = IVenue(obj)
    notes = venue.notes and venue.notes.output_relative_to(obj) or u''
    if notes:
        transforms = getToolByName(obj, 'portal_transforms')
        body_plain = transforms.convertTo(
            'text/plain',
            notes,
            mimetype='text/html',
        ).getData().strip()
        notes = body_plain
    parts = [
        safe_unicode(address),
        safe_unicode(meta_basic.title),
        safe_unicode(meta_basic.description),
        safe_unicode(notes)
    ]
    ret = _concat_and_utf8(*parts)
    return ret
