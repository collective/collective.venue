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

        location_behavior = ILocation(self.context)
        location_ref = location_behavior.location_ref
        if location_ref:
            item = location_ref.to_object
        else:
            item = None

        ret = None
        if item:
            basic = IBasic(item, None)
            locationstring = utils.join_nonempty(
                [basic.title, utils.get_venue_address_string(item)], sep=u', '
            )
            ret = {
                'value': locationstring,
                'parameters': {'altrep': item.absolute_url()},
            }
        else:
            ret = {'value': location_behavior.location_notes}

        return ret

    @property
    def contact(self):
        if not IOrganizer.providedBy(self.context):
            return super(VenueICalendarEventComponent, self).contact

        organizer_behavior = IOrganizer(self.context)
        organizer_ref = organizer_behavior.organizer_ref
        if not organizer_ref:
            return None
        item = organizer_ref.to_object

        ret = None
        if item:
            basic = IBasic(item, None)
            retstring = utils.join_nonempty(
                [basic.title, utils.get_venue_contact_string(item)], sep=u', '
            )
            ret = {'value': retstring}
        else:
            ret = {'value': organizer_behavior.organizer_notes}

        return ret

    @property
    def geo(self):
        if not ILocation.providedBy(self.context):
            return super(VenueICalendarEventComponent, self).geo

        location_behavior = ILocation(self.context)
        location_ref = location_behavior.location_ref
        if location_ref:
            item = location_ref.to_object
        else:
            item = None

        if not IGeolocatable.providedBy(item):
            return super(VenueICalendarEventComponent, self).geo

        geo = IGeolocatable(item, None)
        ret = (geo.geolocation.latitude, geo.geolocation.longitude)
        return {'value': ret}
