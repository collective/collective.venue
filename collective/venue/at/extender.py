try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
try:
    from plone.app.event.at.interfaces import IATEvent
    from plone.app.event import messageFactory as _
except ImportError:
    from Products.ATContentTypes.interfaces import IATEvent
    from Products.ATContentTypes import ATCTMessageFactory as _
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.app.event.at.content import EventAccessor
from zope.component import adapts
from zope.interface import implements
from collective.venue.interfaces import IVenue


class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    pass


class ATEventExtender(object):
    implements(IOrderableSchemaExtender)
    adapts(IATEvent)

    fields = [
        ReferenceFieldExtender("location",
            required=False,
            searchable=False,
            languageIndependent=True,
            relationship='isVenueForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            addable=True,
            widget=ReferenceBrowserWidget(
                description='',
                label=_(u'label_event_location', default=u'Event Location'),
                base_query={'object_provides': IVenue.__identifier__,
                            'sort_on': 'sortable_title'},
                allow_search=True,
                allow_browse=False,
                force_close_on_insert=True,
                show_results_without_query=True,
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

        order = move_after(order, 'location', 'recurrence')
        # This, if above makes problems
        # order = None
        # try:
        #    order = move_after(order, 'location', 'wholeDay', )
        # except XXXError:
        #    order = move_after(order, 'location', 'endDate',
        #               schemata_from='categorization'
        #               schemata_to='default')
        return order


class VenueEventAccessor(EventAccessor):

    @property
    def location(self):
        location = self.context.getLocation()
        if not location:
            return None
        if isinstance(location, basestring):
            # graceful handling in case of unmigrated ATEvent objects.
            return location
        else:
            meta = IDublinCore(location)
            add = IAddress(location)
            return '%s, %s, %s %s, %s' % (
                meta.title,
                add.street,
                add.zip_code,
                add.city,
                get_pycountry_name(add.country) or ''
            )
