from collective.venue import utils
from collective.venue.behaviors import ILocation
from collective.venue.behaviors import IOrganizer
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.ical.exporter import ICalendarEventComponent
from plone.app.uuid.utils import uuidToObject
from plone.event.interfaces import IICalendarEventComponent
from zope.interface import implementer


try:
    from collective.geolocationbehavior.geolocation import IGeolocatable
except ImportError:
    IGeolocatable = None


@implementer(IICalendarEventComponent)
class VenueICalendarEventComponent(ICalendarEventComponent):
    """Returns an icalendar object of the event.
    """

    @property
    def location(self):
        if not ILocation.providedBy(self.context):
            return super(VenueICalendarEventComponent, self).location

        ref = ILocation(self.context)
        item = uuidToObject(ref.location_uid)

        ret = None
        if item:
            basic = IBasic(item, None)
            locationstring =  utils.join_nonempty([
                basic.title,
                utils.get_venue_address_string(item)
            ], sep=u', ')
            ret = {
                'value': locationstring,
                'parameters': {'altrep': item.absolute_url()}
            }
        else:
            ret = {'value': ref.location_notes}

        return ret

    @property
    def contact(self):
        if not IOrganizer.providedBy(self.context):
            return super(VenueICalendarEventComponent, self).contact

        ref = IOrganizer(self.context)
        item = uuidToObject(ref.organizer_uid)

        ret = None
        if item:
            basic = IBasic(item, None)
            retstring =  utils.join_nonempty([
                basic.title,
                utils.get_venue_contact_string(item)
            ], sep=u', ')
            ret = {'value': retstring}
        else:
            ret = {'value': ref.organizer_notes}

        return ret

    @property
    def geo(self):
        if not ILocation.providedBy(self.context):
            return super(VenueICalendarEventComponent, self).geo

        ref = ILocation(self.context)
        item = uuidToObject(ref.location_uid)

        if not IGeolocatable.providedBy(item):
            return super(VenueICalendarEventComponent, self).geo

        geo = IGeolocatable(item, None)
        ret = (
            geo.geolocation.latitude,
            geo.geolocation.longitude
        )
        return {'value': ret}
