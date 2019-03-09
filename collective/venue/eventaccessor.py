# -*- coding: utf-8 -*-
from .utils import join_nonempty
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.venue.behaviors import ILocation
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.uuid.utils import uuidToObject
from plone.event.interfaces import IEventAccessor
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer


@adapter(ILocation)
@implementer(IEventAccessor)
class VenueEventAccessor(EventAccessor):
    def __init__(self, context):
        super(VenueEventAccessor, self).__init__(context)
        del self._behavior_map['location']

    @property
    def _location_link_template(self):
        return u'<a class="pat-plone-modal" href="{url}" title="{address}">{title}</a>'  # noqa

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
        ret = u''
        if meta_basic and add:
            # I'm a location reference.
            # Create a link with href, title and urltext.

            # construct url to location
            site = getSite()
            location_url = location.absolute_url()
            site_path = u'/'.join(site.getPhysicalPath())
            location_path = u'/'.join(location.getPhysicalPath())
            if site_path not in location_path:
                # location in different site - cannot directly open it
                location_url = u'{0}/@@venue_view?uid={1}'.format(
                    site.absolute_url(), location_uid
                )

            country = get_pycountry_name(add.country)
            ret = self._location_link_template.format(  # noqa
                url=location_url,
                address=join_nonempty(
                    (
                        add.street,
                        join_nonempty((add.zip_code, add.city), sep=u' '),
                        country,
                    ),
                    sep=u', ',
                ),
                title=meta_basic.title,
            )

        ret = safe_unicode(ret)
        location_notes = safe_unicode(location_notes)

        ret = join_nonempty([ret, location_notes], u'. ')

        return ret

    @location.setter
    def location(self, value):
        acc = ILocation(self.context)
        acc.location_notes = safe_unicode(value)
