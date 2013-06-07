from plone.indexer import indexer
from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IBasic


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    meta_basic = IBasic(obj)
    text = ''
    text += '%s\n' % address
    text += '%s\n' % meta_basic.title
    text += '%s\n' % meta_basic.description
    return text.strip()
