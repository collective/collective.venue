from collective.venue import messageFactory as _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class IVenue(model.Schema):
    """Marker schema interface for Venue types."""
    notes = RichText(
        title=_(
            u'label_notes',
            default=u'Notes'
        ),
        description=_(
            u'help_notes',
            default=u'Additional notes for the address.'
        ),
        required=False,
    )


class IVenueSettings(Interface):
    """Controlpanel schema for venue types.
    """

    search_base = schema.Choice(
        title=_(
            u'label_search_base',
            default=u'Location Search Base'
        ),
        description=_(
            u'help_search_base',
            u"Path, from which venue types should be searched. Useful for "
            u"lineage multisites to seperate main from childsite venue "
            u"folders. Keep empty to search anywhere."
        ),
        required=False,
        vocabulary='collective.venue.SearchBaseVocabulary'
    )
    default_venue = schema.Choice(
        title=_(
            u'label_default_venue',
            default=u'Default Location'
        ),
        description=_(
            u'help_default_venue',
            u"Default location to be used in events."),
        required=False,
        vocabulary='collective.venue.DefaultVenueVocabulary'
    )


class IVenueLayer(Interface):
    """A Browserlayer indicating that this product is actually installed via
    Generic Setup.
    """
