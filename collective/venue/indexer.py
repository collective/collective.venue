from plone.indexer import indexer
from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IDublinCore


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    acc = IDublinCore(obj)
    text = ''
    text += '%s\n' % address
    text += '%s\n' % acc.title
    text += '%s\n' % acc.description
    return text.strip()
