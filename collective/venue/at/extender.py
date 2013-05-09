from zope.component import adapts
from zope.interface import implements

try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes import ATCTMessageFactory as _
try:
    from plone.app.event.at.interfaces import IATEvent
except:
    from Products.ATContentTypes.interfaces import IATEvent
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.field import ExtensionField

from archetypes.referencebrowserwidget import ReferenceBrowserWidget

class ReferenceFieldExtender(ExtensionField, atapi.ReferenceField):
    pass


class ATEventExtender(object):
    implements(IOrderableSchemaExtender)
    adapts(IATEvent)

    fields = [
        ReferenceFieldExtender("location",
            required=False,
            searchable=True,
            languageIndependent=True,
            relationship='isVenueForEvent',
            multiValued=False,
            allowed_types=('Venue',),
            addable=True,
            #vocabulary_display_path_bound=-1,  # Avoid silly Archetypes object
            #                                   # title magic
            #enforceVocabulary=True,
            widget=ReferenceBrowserWidget(
                description='',
                label=_(u'label_event_location', default=u'Event Location'),
            ),
            #widget=atapi.ReferenceWidget(
            #description='',
            #    label=_(u'label_event_location', default=u'Event Location'),
            #    checkbox_bound=1,  # use selection widget
            #    destination_types=['Venue'],
            #    addable=True,
            #    ),
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

        return move_after(order, 'location', 'endDate')


class ATEventModifier(object):
    implements(ISchemaModifier)
    adapts(IATEvent)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        #schema['location'].widget.visible = {'view': 'hidden',
        #                                     'edit': 'hidden'}
        schema['contactName'].widget.visible = {'view': 'hidden',
                                                'edit': 'hidden'}
        schema['contactEmail'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
        schema['contactPhone'].widget.visible = {'view': 'hidden',
                                                 'edit': 'hidden'}
