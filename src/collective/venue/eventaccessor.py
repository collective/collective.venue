from .utils import join_nonempty
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.venue.behaviors import ILocation
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.uuid.utils import uuidToObject
from plone.event.interfaces import IEventAccessor
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer


@adapter(ILocation)
@implementer(IEventAccessor)
class VenueEventAccessor(EventAccessor):
    def __init__(self, context):
        super().__init__(context)
        del self._behavior_map["location"]

    @property
    def _location_link_template(self):
        return '<a class="pat-plone-modal" href="{url}" title="{address}">{title}</a>'

    @property
    def location(self):
        context = self.context
        location_ref = ILocation(context, None)
        if not location_ref:
            return
        location_uid = location_ref.location_uid
        location_notes = location_ref.location_notes
        location = uuidToObject(location_uid)

        meta_basic = IBasic(location, None)
        add = IAddress(location, None)

        location_url = None
        ret = ""
        if meta_basic and add:
            # I'm a location reference.
            # Create a link with href, title and urltext.

            # construct url to location
            site = getSite()
            location_url = location.absolute_url()
            site_path = "/".join(site.getPhysicalPath())
            location_path = "/".join(location.getPhysicalPath())
            if site_path not in location_path:
                # location in different site - cannot directly open it
                location_url = f"{site.absolute_url()}/@@venue_view?uid={location_uid}"

            country = get_pycountry_name(add.country)
            ret = self._location_link_template.format(
                url=location_url,
                address=join_nonempty(
                    (
                        add.street,
                        join_nonempty((add.zip_code, add.city), sep=" "),
                        country,
                    ),
                    sep=", ",
                ),
                title=meta_basic.title,
            )

        ret = join_nonempty([ret, location_notes], ". ")

        return ret

    @location.setter
    def location(self, value):
        acc = ILocation(self.context)
        acc.location_notes = value
