from Acquisition import aq_parent
from Products.CMFPlone.utils import safe_unicode
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.at.content import EventAccessor
from plone.app.event.at.interfaces import IATEvent
from plone.app.event.dx.interfaces import IDXEvent
from plone.event.interfaces import IOccurrence


class VenueEventAccessor(EventAccessor):

    @property
    def location(self):
        context = self.context
        location = None
        location_notes = None
        if IATEvent.providedBy(context):
            location = context.getLocation()
            if hasattr(context, 'location_notes'):
                location_notes = context.location_notes()
                # Else location_notes not stored on context
        elif IDXEvent.providedBy(context):
            from plone.app.event.dx.behaviors import IEventLocation
            location = IEventLocation(context).location
            location_notes = ''  # not implemented yet

        meta_basic = IBasic(location, None)
        add = IAddress(location, None)

        if meta_basic and add:
            # I'm a location reference.
            country = get_pycountry_name(add.country)
            location = safe_unicode('%s%s%s%s%s' % (
                meta_basic.title,
                add.street and ', %s' % add.street or '',
                add.zip_code and ', %s' % add.zip_code or '',
                add.city and ' %s' % add.city or '',
                country and ', %s' % country or ''
            ))

        location = safe_unicode(location)
        location_notes = safe_unicode(location_notes)
        location = '%s%s%s' % (location and location or '',
                               location and location_notes and ', ' or '',
                               location_notes and location_notes or '')
        return location


def get_location(context):
    """In case location is not of type basestring, it's propably a
    reference, which case we handle here.
    """
    # Get the original location directly from the context, as in case of a
    # reference, the accessor might return an string representing the
    # location instead of the referenced object.
    location = None
    location_notes = None
    if IOccurrence.providedBy(context):
        # Get location from real object
        context = aq_parent(context)
    if IATEvent.providedBy(context):
        location = context.getLocation()
        if hasattr(context, 'location_notes'):
            location_notes = context.location_notes()
            # Else location_notes not stored on context
    elif IDXEvent.providedBy(context):
        from plone.app.event.dx.behaviors import IEventLocation
        location = IEventLocation(context).location
        location_notes = ''  # not implemented yet

    meta_basic = IBasic(location, None)
    add = IAddress(location, None)

    if meta_basic and add:
        # I'm a location reference.
        # Create a link with href, title, urltext, but don't use
        # IEventAccessor.location for the title, as it contains redundant
        # information. We don't want to display the Venue Title again.
        country = get_pycountry_name(add.country)
        location = '<a class="venue_ref_popup" href="%s" title="%s">%s</a>' % (
            location.absolute_url(),
            '%s%s%s%s' % (
                add.street and add.street or '',
                add.zip_code and ', %s' % add.zip_code or '',
                add.city and ' %s' % add.city or '',
                country and ', %s' % country or '',
            ),
            meta_basic.title,
        )
    # Else: graceful handling of location as basestring in case of unmigrated
    # ATEvent objects.

    location = safe_unicode(location)
    location_notes = safe_unicode(location_notes)
    location = '%s%s%s' % (location and location or '',
                         location and location_notes and ', ' or '',
                         location_notes and location_notes or '')
    return location


# PATCH
from plone.app.event.browser import event_view
ORIG_get_location = event_view.get_location
event_view.get_location = get_location
