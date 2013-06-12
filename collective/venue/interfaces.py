from plone.dexterity.interfaces import IDexteritySchema
from zope.interface import Interface

class IVenue(IDexteritySchema):
    """Marker schema interface for Venue types."""


class IVenueLayer(Interface):
   """A Browserlayer indicating that this product is actually installed via
   Generic Setup.
   """
