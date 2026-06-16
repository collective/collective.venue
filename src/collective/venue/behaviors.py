from collective.venue import _
from collective.venue.interfaces import IVenueEnabled
from collective.venue.utils import get_base_path
from plone import api
from plone.app.event.dx.interfaces import IDXEvent
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def default_location(context):
    """Provide default location."""
    default = api.portal.get_registry_record("collective.venue.default_venue")
    return default or ""


@provider(IFormFieldProvider)
class ILocation(model.Schema, IVenueEnabled, IDXEvent):

    location_uid = schema.Choice(
        title=_("label_event_location", default="Location"),
        description=_("description_event_location", default="Select a location."),
        required=False,
        missing_value="",
        defaultFactory=default_location,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    form.widget(
        "location_uid",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Venue"],
            "basePath": get_base_path,
        },
    )

    location_notes = schema.Text(
        title=_("label_event_location_notes", default="Location notes"),
        description=_(
            "description_event_location_notes",
            default="One-time location or additional Information.",
        ),
        required=False,
        default=None,
    )
    directives.fieldset(
        "venue",
        label=_("fieldset_venue", default="Location/Organizer"),
        fields=["location_uid", "location_notes"],
    )


@provider(IContextAwareDefaultFactory)
def default_organizer(context):
    """Provide default organizer."""
    default = api.portal.get_registry_record("collective.venue.default_organizer")
    return default or ""


@provider(IFormFieldProvider)
class IOrganizer(model.Schema, IVenueEnabled):

    organizer_uid = schema.Choice(
        title=_("label_event_organizer", default="Organizer"),
        description=_("description_event_organizer", default="Select an organizer."),
        required=False,
        missing_value="",
        defaultFactory=default_organizer,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    form.widget(
        "organizer_uid",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Venue"],
            "basePath": get_base_path,
        },
    )

    organizer_notes = schema.Text(
        title=_("label_event_organizer_notes", default="Organizer notes"),
        description=_(
            "description_event_organizer_notes",
            default="One-time organizer or additional Information.",
        ),
        required=False,
        default=None,
    )
    directives.fieldset(
        "venue",
        label=_("fieldset_venue", default="Location/Organizer"),
        fields=["organizer_uid", "organizer_notes"],
        order=10,
    )
