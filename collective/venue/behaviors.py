from collective.venue import messageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides
from plone.app.widgets.dx import AjaxSelectFieldWidget
from plone.autoform import directives as form


class ILocation(model.Schema):

    location = schema.Tuple(
        label=_(u'label_event_location', default=u'Event Location'),
        description=_(
            u'description_event_location',
            default=u'Reference to an existing location.'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget('location', AjaxSelectFieldWidget,
                vocabulary='collective.venue.venues')

    location_notes = schema.Text(
        label=_(
            u'label_event_location_notes',
            default=u'Notes for the Venue'),
        description=_(
            u'description_event_location_notes',
            default=u'Additional Information for the Venue.'),
        required=False,
        missing_value=u'',
    )
alsoProvides(ILocation, IFormFieldProvider)
