from collective.tiles.collection.interfaces import ICollectionTileRenderer
from collective.venue import messageFactory
from plone.tiles.tile import Tile
from Products.Five.browser import BrowserView
from zope.interface import implementer

from .venue import VenueView


class VenueTile(VenueView, Tile):
    def __init__(self, context, request):
        super(VenueTile, self).__init__(context, request)
        # This method is not necessary, but if you have to debug something,
        # place a pdb here.


@implementer(ICollectionTileRenderer)
class VenueCollectionTileView(BrowserView):
    display_name = messageFactory('Venue collection layout')
