try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi

try:
    from plone.app.event.at.interfaces import IATEvent
except ImportError:
    from Products.ATContentTypes.interfaces import IATEvent
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from collective.venue import messageFactory as _
from collective.venue.interfaces import IVenue
from collective.venue.interfaces import IVenueLayer
from zope.component import adapts
from zope.interface import implements


def base_query_venue():
    base_query = {}
    base_query['object_provides'] = IVenue.__identifier__
    base_query['sort_on'] = 'sortable_title'
    return base_query


class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    pass


class TextFieldExtender(ExtensionField, atapi.TextField):
    pass


class ATEventExtender(object):
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    adapts(IATEvent)
    layer = IVenueLayer  # Only apply if product is installed

    fields = [
        ReferenceFieldExtender(
            "location",
            required=False,
            searchable=False,
            languageIndependent=True,
            relationship='isVenueForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            addable=True,
            widget=ReferenceBrowserWidget(
                label=_(u'label_event_location', default=u'Event Location'),
                description=_(
                    u'description_event_location',
                    default=u'Reference to an existing location.'),
                base_query=base_query_venue,
                allow_search=True,
                allow_browse=False,
                force_close_on_insert=True,
                show_results_without_query=True,
            ),
        ),

        TextFieldExtender(
            'location_notes',
            required=False,
            searchable=True,
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            widget=atapi.TextAreaWidget(
                label=_(
                    u'label_event_location_notes',
                    default=u'Notes for the Venue'),
                description=_(
                    u'description_event_location_notes',
                    default=u'Additional Information for the Venue.'),
                rows=2,
                allow_file_upload=False,
                ),
            ),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, order):

        def move_after(order,
                       new_field, after_field,
                       schemata_from='default',
                       schemata_to=None):
            s_from = order[schemata_from]
            if schemata_to:
                s_to = order[schemata_to]
            else:
                s_to = s_from
            s_from.remove(new_field)
            idx = s_to.index(after_field)
            s_to.insert(idx + 1, new_field)
            return order

        loc_from = 'default'
        loc_to = 'default'
        if 'location' in order['categorization']:
            # Fix, if location still in categorization
            loc_from = 'categorization'
        order = move_after(order, 'location', 'recurrence',
                           schemata_from=loc_from, schemata_to=loc_to)
        order = move_after(order, 'location_notes', 'location')

        # This, if above causes troubles
        # order = None
        # try:
        #    order = move_after(order, 'location', 'wholeDay', )
        # except XXXError:
        #    order = move_after(order, 'location', 'endDate',
        #               schemata_from='categorization'
        #               schemata_to='default')

        return order
