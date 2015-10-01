from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.indexer import indexer
# from collective.venue.behaviors import ILocation


# @indexer(ILocation)
# def venue_indexer(obj):
#     return ILocation(obj).location


def _concat_and_utf8(*args):
    """Concats args with spaces between and returns utf-8 string, it does not
    matter if input was unicode or str.
    Taken from ``plone.app.contenttypes.indexers``
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        if value:
            result = ' '.join((result, value))
    return result


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    meta_basic = IBasic(obj)
    venue = IVenue(obj)
    notes = venue.notes and venue.notes.output or u''
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
