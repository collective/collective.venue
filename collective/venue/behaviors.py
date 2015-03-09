from collective.venue import messageFactory as _
from collective.venue.interfaces import IVenue
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.widgets.dx import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides


class ILocation(model.Schema):

    location_uid = schema.Choice(
        title=_(u'label_event_location', default=u'Event Location'),
        description=_(
            u'description_event_location',
            default=u'Reference to an existing location.'),
        required=False,
        source=CatalogSource(object_provides=IVenue.__identifier__),
    )
    form.widget('location_uid', RelatedItemsFieldWidget)

    location_notes = schema.Text(
        title=_(
            u'label_event_location_notes',
            default=u'Notes for the Venue'),
        description=_(
            u'description_event_location_notes',
            default=u'Additional Information for the Venue.'),
        required=False,
        missing_value=u'',
    )
alsoProvides(ILocation, IFormFieldProvider)
