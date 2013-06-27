from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.indexer import indexer


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    venue = IVenue(obj)
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    meta_basic = IBasic(obj)
    text = ''
    text += '%s\n' % address
    text += '%s\n' % meta_basic.title
    text += '%s\n' % meta_basic.description
    text += '%s\n' % venue.notes
    notes = venue.notes and venue.notes.output or None
    if notes:
        transforms = getToolByName(obj, 'portal_transforms')
        body_plain = transforms.convertTo(
            'text/plain',
            notes,
            mimetype='text/html',
            ).getData().strip()
        text += body_plain
    return safe_unicode(text.strip())
