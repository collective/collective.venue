from Products.CMFPlone.utils import safe_unicode
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.venue.behaviors import ILocation
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.event.dx.interfaces import IDXEvent
from plone.app.uuid.utils import uuidToObject
from plone.event.interfaces import IEventAccessor
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer


@adapter(IDXEvent)
@implementer(IEventAccessor)
class VenueEventAccessor(EventAccessor):

    def __init__(self, context):
        super(VenueEventAccessor, self).__init__(context)
        del self._behavior_map['location']

    @property
    def _location_link_template(self):
        return u'<a class="venue_ref_popup" href="{url}" title="{address}">'\
               u'{title}</a>'

    @property
    def location(self):
        context = self.context
        location_ref = ILocation(context)
        location_uid = location_ref.location_uid
        location_notes = location_ref.location_notes
        location = uuidToObject(location_uid)

        site_url = getSite().absolute_url()
        location_url = location.absolute_url()
        if site_url not in location_url:
            # location in different site - cannot directly open it
            location_url = u'{0}/@@venue_view?uid={1}'.format(
                site_url, location_uid)

        meta_basic = IBasic(location, None)
        add = IAddress(location, None)

        ret = u''
        if meta_basic and add:
            # I'm a location reference.
            # Create a link with href, title and urltext.
            country = get_pycountry_name(add.country)
            ret = self._location_link_template.format(  # noqa
                url=location_url,
                address=u', '.join([it for it in [
                    add.street,
                    add.zip_code,
                    add.city,
                    country
                ] if it]),
                title=meta_basic.title,
            )

        ret = safe_unicode(ret)
        location_notes = safe_unicode(location_notes)

        ret = u', '.join([it for it in [
            safe_unicode(ret),
            safe_unicode(location_notes)
        ] if it])
        return ret

    @location.setter
    def location(self, value):
        acc = ILocation(self.context)
        acc.location_notes = safe_unicode(value)
