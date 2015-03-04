from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import Interface
from zope.interface import alsoProvides
from collective.venue import messageFactory as _


class IVenue(model.Schema):
    """Marker schema interface for Venue types."""
    notes = RichText(
        title=_(u'label_notes', default=u'Notes'),
        description=_(u'help_notes',
                      default=u'Additional notes for the address.'),
        required=False,
    )
alsoProvides(IVenue, IFormFieldProvider)


class IVenueLayer(Interface):
    """A Browserlayer indicating that this product is actually installed via
    Generic Setup.
    """
