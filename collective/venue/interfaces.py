# -*- coding: utf-8 -*-
from collective.venue import messageFactory as _
from collective.venue.utils import get_base_path
from collective.venue.utils import get_site
from collective.venue.vocabularies import default_map_layer
from collective.venue.vocabularies import default_map_layers
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import order_after
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
    order_after(notes='*')


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
        default='',
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'search_base',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Folder'],  # better: is_folderish
            'basePath': get_site,
        }
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
        default='',
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'default_venue',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Venue'],
            'basePath': get_base_path,
        }
    )

    default_organizer = schema.Choice(
        title=_(
            u'label_default_organizer',
            default=u'Default Organizer'
        ),
        description=_(
            u'help_default_organizer',
            u"Default organizer to be used in events."),
        required=False,
        default='',
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'default_organizer',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Venue'],
            'basePath': get_base_path,
        }
    )

    google_api_key = schema.TextLine(
        title=_(u'label_google_api_key', default=u'Google maps API Key'),
        description=_(u'help_google_api_key', default=u'If you want to use the Google Maps search API for higher accuracy, you have to provide a Google Maps API key here.'),  # noqa
        required=False,
        default=None
    )

    show_google_maps_link = schema.Bool(
        title=_(u'label_google_maps_link', default=u'Show Google maps link.'),
        description=_(u'help_google_maps_link', default=u'Show a link to the Google Maps site, which can be used for further actions like routing.'),  # noqa
        required=False,
        default=False
    )

    default_map_layer = schema.Choice(
        title=_(
            u'default_map_layer',
            u'Default map layer'
        ),
        description=_(
            u'help_default_map_layer',
            default=u'Set the default map layer'
        ),
        required=False,
        default=default_map_layer,
        vocabulary='collective.venue.map_layers'
    )

    map_layers = schema.List(
        title=_(u'label_map_layers', u'Map Layers'),
        description=_(
            u'help_map_layers',
            default=u'Set the available map layers'),
        required=False,
        default=default_map_layers,
        missing_value=[],
        value_type=schema.Choice(vocabulary='collective.venue.map_layers'))


class IVenueLayer(Interface):
    """A Browserlayer indicating that this product is actually installed via
    Generic Setup.
    """
