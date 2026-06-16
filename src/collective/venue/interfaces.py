from collective.venue import _
from collective.venue.utils import get_base_path
from collective.venue.utils import get_site
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import order_after
from plone.autoform.interfaces import IFormFieldProvider
from plone.event.interfaces import IEvent
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class IVenue(model.Schema):
    """Marker schema interface for Venue types."""

    notes = RichText(
        title=_("label_notes", default="Notes"),
        description=_("help_notes", default="Additional notes for the address."),
        required=False,
    )
    order_after(notes="*")


class IVenueSettings(Interface):
    """Controlpanel schema for venue types."""

    search_base = schema.Choice(
        title=_("label_search_base", default="Location Search Base"),
        description=_(
            "help_search_base",
            "Path, from which venue types should be searched. Useful for "
            "lineage multi sites to separate main from child site venue "
            "folders. Keep empty to search anywhere.",
        ),
        required=False,
        default="",
        vocabulary="plone.app.vocabularies.Catalog",
    )
    form.widget(
        "search_base",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Folder"],  # better: is_folderish
            "basePath": get_site,
        },
    )

    default_venue = schema.Choice(
        title=_("label_default_venue", default="Default Location"),
        description=_("help_default_venue", "Default location to be used in events."),
        required=False,
        default="",
        vocabulary="plone.app.vocabularies.Catalog",
    )
    form.widget(
        "default_venue",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Venue"],
            "basePath": get_base_path,
        },
    )

    default_organizer = schema.Choice(
        title=_("label_default_organizer", default="Default Organizer"),
        description=_(
            "help_default_organizer", "Default organizer to be used in events."
        ),
        required=False,
        default="",
        vocabulary="plone.app.vocabularies.Catalog",
    )
    form.widget(
        "default_organizer",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Venue"],
            "basePath": get_base_path,
        },
    )


class IVenueLayer(Interface):
    """A Browserlayer indicating that this product is actually installed via
    Generic Setup.
    """


class IVenueEnabled(IEvent):
    """Marker interface for objects which provide the ILocation or IOrganizer
    interfaces.
    """
