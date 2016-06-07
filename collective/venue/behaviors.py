from collective.venue import messageFactory as _
from collective.venue.interfaces import IVenue
from collective.venue.vocabularies import VenueSource
from plone import api
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def default_location(context):
    """Provide default location.
    """
    default_venue = api.portal.get_registry_record('collective.venue.default_venue')  # noqa
    return default_venue or ''


@provider(IFormFieldProvider)
class ILocation(model.Schema):

    location_uid = schema.Choice(
        title=_(u'label_event_location', default=u'Location'),
        description=_(
            u'description_event_location',
            default=u'Select a location.'),
        required=False,
        missing_value='',
        defaultFactory=default_location,
        source=VenueSource(object_provides=IVenue.__identifier__),
    )
    form.widget('location_uid', RelatedItemsFieldWidget)

    location_notes = schema.Text(
        title=_(
            u'label_event_location_notes',
            default=u'Location notes'),
        description=_(
            u'description_event_location_notes',
            default=u'Additional Information for the Location.'),
        required=False,
        default=None,
    )
