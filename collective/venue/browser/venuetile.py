from .venue import VenueView
from plone.tiles.tile import Tile


class VenueTile(VenueView, Tile):

    def __init__(self, context, request):
        super(VenueTile, self).__init__(context, request)
        # This method is not necessary, but if you have to debug something,
        # place a pdb here.
